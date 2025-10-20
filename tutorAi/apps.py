from django.apps import AppConfig
import os
import shutil


class TutorAiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tutorAi'

    def ready(self):
        """
        Runs automatically when Django starts.
        Cleans up vector store and temp files.
        """
        from django.conf import settings

        # 1️⃣ Delete temp PDFs
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                os.makedirs(temp_dir, exist_ok=True)
                print("🗑️ Cleared media/temp folder.")
            except Exception as e:
                print(f"⚠️ Failed to clear media/temp: {e}")

        # 2️⃣ Delete Chroma vector database inside tutorAi/components/
        vector_dir = os.path.join(settings.BASE_DIR, 'tutorAi', 'components', 'vector_store_db')
        if os.path.exists(vector_dir):
            try:
                shutil.rmtree(vector_dir)
                print("🧠 Cleared Chroma vector database.")
            except Exception as e:
                print(f"⚠️ Failed to clear vector store: {e}")

        print("✅ Startup cleanup completed successfully.")
