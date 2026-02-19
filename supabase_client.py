from supabase import create_client
import uuid
import os

SUPABASE_URL = "https://pfecxmgqmtsjmkyqutmk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBmZWN4bWdxbXRzam1reXF1dG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1MjMyMjMsImV4cCI6MjA4NzA5OTIyM30.90Pzb2JbseLrQKECANEtVT-qGDVMCNvy_h0HlEnZkTQ"   # ⚠ Replace with regenerated key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- DATABASE FUNCTIONS ----------------

def insert_inspection(data):
    return supabase.table("inspections").insert(data).execute()

def get_all_inspections():
    return supabase.table("inspections").select("*").order("created_at", desc=True).execute()

def delete_inspection(record_id):
    return supabase.table("inspections").delete().eq("id", record_id).execute()

# ---------------- AUTH ----------------

def login_user(email, password):
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    if response.user is None:
        return None

    return response

# ---------------- STORAGE UPLOAD ----------------

def upload_file(bucket_name, file_path):
    """
    Upload file to Supabase Storage and return public URL
    """

    file_extension = os.path.splitext(file_path)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    with open(file_path, "rb") as f:
        supabase.storage.from_(bucket_name).upload(unique_filename, f)

    public_url = supabase.storage.from_(bucket_name).get_public_url(unique_filename)

    return public_url
