from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    ssl_mode: str
    
    class Config:
        env_file = ".env"
        
class EmailSettings(BaseSettings):
    smtp_host: str = "your_smtp_host"
    smtp_port: int = 587  # or use the appropriate port for your email service
    smtp_username: str = "your_email_username"
    smtp_password: str = "your_email_password"
    smtp_tls: bool = True
    email_from: str = "your_email@example.com"

    
settings = Settings()