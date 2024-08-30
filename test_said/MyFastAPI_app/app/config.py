import bcrypt

# Nom de l'index Elasticsearch pour les offres d'emploi
JOBMARKET_INDEX = "jobmarket"

# Hachage des mots de passe des utilisateurs admin
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Vérification des mots de passe hachés
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Utilisateurs admin avec mots de passe hachés
admins = {
    "admin": hash_password("@dmin7")
}
