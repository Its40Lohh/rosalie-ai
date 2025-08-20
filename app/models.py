from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	email = Column(String(120), unique=True, nullable=False)
	password_hash = Column(String(256), nullable=False)
	preferences = Column(JSON, nullable=True)
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
	updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
	
	# Relationships
	businesses = relationship("Business", back_populates="user")
	financial_accounts = relationship("FinancialAccount", back_populates="user")
	mood_entries = relationship("MoodEntry", back_populates="user")
	notifications = relationship("Notification", back_populates="user")
	conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
	__tablename__ = 'conversations'
	
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	message = Column(Text, nullable=False)
	response = Column(Text, nullable=False)
	timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
	context = Column(Text, nullable=True)
	
	# Relationship
	user = relationship("User", back_populates="conversations")

class Notification(Base):
	__tablename__ = 'notifications'
	
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	title = Column(String(200), nullable=False)
	message = Column(Text, nullable=False)
	notification_type = Column(String(50), nullable=False)
	is_read = Column(Boolean, nullable=False, default=False)
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
	read_at = Column(DateTime, nullable=True)
	
	# Relationship
	user = relationship("User", back_populates="notifications")

class MoodEntry(Base):
	__tablename__ = 'mood_entries'
	
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	mood_rating = Column(Integer, nullable=False)  # e.g., 1-10 scale
	energy_level = Column(Integer, nullable=False)  # e.g., 1-10 scale
	notes = Column(Text, nullable=True)
	entry_date = Column(DateTime, nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
	
	# Relationship
	user = relationship("User", back_populates="mood_entries")

class FinancialAccount(Base):
	__tablename__ = 'financial_accounts'
	
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	institution_name = Column(String(200), nullable=False)
	account_type = Column(String(50), nullable=False)
	account_number_masked = Column(String(50), nullable=False)
	balance = Column(Float, nullable=False, default=0.0)
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
	is_active = Column(Boolean, nullable=False, default=True)
	
	# Relationships
	user = relationship("User", back_populates="financial_accounts")
	transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
	__tablename__ = 'transactions'
	
	id = Column(Integer, primary_key=True)
	account_id = Column(Integer, ForeignKey('financial_accounts.id'), nullable=False)
	amount = Column(Float, nullable=False)
	description = Column(String(255), nullable=False)
	category = Column(String(100), nullable=False)
	transaction_date = Column(DateTime, nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
	is_income = Column(Boolean, nullable=False)
	
	# Relationship
	account = relationship("FinancialAccount", back_populates="transactions")

class Business(Base):
	__tablename__ = 'businesses'
	
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	name = Column(String(200), nullable=False)
	description = Column(Text, nullable=True)
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
	is_active = Column(Boolean, nullable=False, default=True)
	
	# Relationships
	user = relationship("User", back_populates="businesses")
	projects = relationship("Project", back_populates="business")

class Project(Base):
	__tablename__ = 'projects'
	
	id = Column(Integer, primary_key=True)
	business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
	name = Column(String(200), nullable=False)
	description = Column(Text, nullable=True)
	status = Column(String(50), nullable=False, default='pending')
	priority = Column(String(20), nullable=False, default='medium')
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
	deadline = Column(DateTime, nullable=True)
	progress_percentage = Column(Integer, nullable=False, default=0)
	
	# Relationships
	business = relationship("Business", back_populates="projects")
	tasks = relationship("Task", back_populates="project")

class Task(Base):
	__tablename__ = 'tasks'
	
	id = Column(Integer, primary_key=True)
	project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
	title = Column(String(200), nullable=False)
	description = Column(Text, nullable=True)
	status = Column(String(50), nullable=False, default='pending')
	priority = Column(String(20), nullable=False, default='medium')
	estimated_hours = Column(Float, nullable=True)
	actual_hours = Column(Float, nullable=True, default=0.0)
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
	due_date = Column(DateTime, nullable=True)
	completed_at = Column(DateTime, nullable=True)
	
	# Relationship
	project = relationship("Project", back_populates="tasks")
