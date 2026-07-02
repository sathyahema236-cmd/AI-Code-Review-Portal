import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file,flash
)

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from database.db import get_connection
from utils.gemini_ai import review_code


app = Flask(__name__)
app.secret_key = "AI_CODE_REVIEW_SECRET_KEY_2026"

# ---------------- CONFIGURATION ---------------- #

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ---------------- #
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM users WHERE email=%s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:

            if check_password_hash(user["password"], password):

                session["user_email"] = user["email"]
                session["user_name"] = user["full_name"]

                return redirect(url_for("dashboard"))

            else:
               flash("Incorrect Password!", "danger")
            return redirect(url_for("login"))

        else:
            flash("User not found. Please register first.", "warning")
        return redirect(url_for("login"))

    return render_template("login.html")

# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if email already exists
        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()

            flash("Email already registered!", "warning")
            return redirect(url_for("register"))

        # Insert new user
        sql = """
        INSERT INTO users(full_name, email, password)
        VALUES(%s, %s, %s)
        """

        cursor.execute(sql, (full_name, email, password))
        conn.commit()

        cursor.close()
        conn.close()

        flash("Registration Successful! Please Login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "user_email" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Uploaded files
    cursor.execute("""
        SELECT *
        FROM uploaded_files
        WHERE user_email=%s
        ORDER BY uploaded_at DESC
    """, (session["user_email"],))

    files = cursor.fetchall()

    # Count uploaded files
    cursor.execute("""
        SELECT COUNT(*) AS total_files
        FROM uploaded_files
        WHERE user_email=%s
    """, (session["user_email"],))

    total_files = cursor.fetchone()["total_files"]

    # Count reviews
    cursor.execute("""
        SELECT COUNT(*) AS total_reviews
        FROM reviews
    """)

    total_reviews = cursor.fetchone()["total_reviews"]

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        files=files,
        user_name=session["user_name"],
        total_files=total_files,
        total_reviews=total_reviews
    )
@app.route("/profile")
def profile():

    if "user_email" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT full_name, email
    FROM users
    WHERE email=%s
    """

    cursor.execute(sql, (session["user_email"],))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "profile.html",
        user=user
    )
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["admin"] = True
            return redirect(url_for("admin_dashboard"))

    return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) total FROM users")
    total_users = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) total FROM reviews")
    total_reviews = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) total FROM uploaded_files")
    total_files = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_reviews=total_reviews,
        total_files=total_files
    )

@app.route("/reviews")
def reviews():

    if "user_email" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if search:

        sql = """
        SELECT *
        FROM reviews
        WHERE file_name LIKE %s
        ORDER BY created_at DESC
        """

        cursor.execute(sql, ("%" + search + "%",))

    else:

        sql = """
        SELECT *
        FROM reviews
        ORDER BY created_at DESC
        """

        cursor.execute(sql)

    reviews = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "reviews.html",
        reviews=reviews,
        search=search
    )
@app.route("/review/<int:review_id>")
def view_review(review_id):

    if "user_email" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT *
    FROM reviews
    WHERE id=%s
    """

    cursor.execute(sql, (review_id,))
    review = cursor.fetchone()

    cursor.close()
    conn.close()

    if review is None:
        return "Review Not Found"

    return render_template(
        "review.html",
        filename=review["file_name"],
        review=review["review"]
    )
@app.route("/download_review/<int:review_id>")
def download_review(review_id):

    if "user_email" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM reviews WHERE id=%s",
        (review_id,)
    )

    review = cursor.fetchone()

    cursor.close()
    conn.close()

    if review is None:
        return "Review Not Found"

    pdf_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        f"review_{review_id}.pdf"
    )

    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Code Review Report",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            f"<b>File Name:</b> {review['file_name']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph("<br/>", styles["Normal"])
    )

    story.append(
        Paragraph(
            review["review"].replace("\n", "<br/>"),
            styles["Normal"]
        )
    )

    doc.build(story)

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"{review['file_name']}_Review.pdf"
    )
@app.route("/delete_review/<int:review_id>")
def delete_review(review_id):

    if "user_email" not in session:
        return redirect(url_for("login"))

    conn = get_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM reviews WHERE id=%s"

    cursor.execute(sql, (review_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("reviews"))

# ---------------- FILE UPLOAD ---------------- #

@app.route("/upload", methods=["POST"])
def upload():

    if "code_file" not in request.files:
        return "No file selected."

    file = request.files["code_file"]

    if file.filename == "":
        return "Please choose a file."

    if not file.filename.endswith(".py"):
        return "Only Python (.py) files are allowed."

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    # ---------------- SAVE FILE DETAILS ---------------- #

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO uploaded_files
    (user_email,file_name,file_path)
    VALUES(%s,%s,%s)
    """

    cursor.execute(
        sql,
        (
           session["user_email"],
            filename,
            filepath
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    # ---------------- READ PYTHON FILE ---------------- #

    try:

        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

    except Exception as e:

        return f"Error reading file: {e}"

    # ---------------- GEMINI AI REVIEW ---------------- #

    try:

        review = review_code(code)

    except Exception as e:

        return f"Gemini Error: {e}"

    # ---------------- SAVE REVIEW IN DATABASE ---------------- #

    try:

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO reviews(file_name, review)
        VALUES(%s,%s)
        """

        cursor.execute(sql, (filename, review))

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:

        return f"Database Error: {e}"

    # ---------------- SHOW REVIEW PAGE ---------------- #

    return render_template(
        "review.html",
        filename=filename,
        review=review
    )


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)