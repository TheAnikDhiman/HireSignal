"""Initial 6-table PostgreSQL schema for HireSignal

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 1. resumes
    op.create_table(
        'resumes',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('candidate_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('linkedin_url', sa.String(length=255), nullable=True),
        sa.Column('github_url', sa.String(length=255), nullable=True),
        sa.Column('file_name', sa.String(length=255), nullable=True),
        sa.Column('file_type', sa.String(length=50), nullable=False, server_default='plain_text'),
        sa.Column('raw_text', sa.Text(), nullable=False),
        sa.Column('cleaned_text', sa.Text(), nullable=True),
        sa.Column('total_experience_years', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_resumes_candidate_name', 'resumes', ['candidate_name'])
    op.create_index('ix_resumes_email', 'resumes', ['email'])

    # 2. job_descriptions
    op.create_table(
        'job_descriptions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('company', sa.String(length=255), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('seniority_level', sa.String(length=50), nullable=True),
        sa.Column('raw_text', sa.Text(), nullable=False),
        sa.Column('cleaned_text', sa.Text(), nullable=True),
        sa.Column('required_experience_years', sa.Float(), nullable=True),
        sa.Column('required_skills', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_job_descriptions_title', 'job_descriptions', ['title'])

    # 3. skills
    op.create_table(
        'skills',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('aliases', sa.JSON(), nullable=True),
        sa.Column('weight', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('is_technical', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    op.create_index('ix_skills_slug', 'skills', ['slug'])
    op.create_index('ix_skills_category', 'skills', ['category'])

    # 4. resume_skills
    op.create_table(
        'resume_skills',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('resume_id', sa.String(length=36), nullable=False),
        sa.Column('skill_id', sa.String(length=36), nullable=False),
        sa.Column('frequency', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('context_snippet', sa.Text(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('resume_id', 'skill_id', name='uq_resume_skill')
    )
    op.create_index('ix_resume_skills_resume_id', 'resume_skills', ['resume_id'])
    op.create_index('ix_resume_skills_skill_id', 'resume_skills', ['skill_id'])

    # 5. scores
    op.create_table(
        'scores',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('resume_id', sa.String(length=36), nullable=False),
        sa.Column('job_description_id', sa.String(length=36), nullable=False),
        sa.Column('overall_fit_score', sa.Float(), nullable=False),
        sa.Column('tfidf_similarity', sa.Float(), nullable=False),
        sa.Column('skill_overlap_score', sa.Float(), nullable=False),
        sa.Column('red_flag_penalty', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('matched_skills_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('missing_skills_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('matched_skills', sa.JSON(), nullable=True),
        sa.Column('missing_skills', sa.JSON(), nullable=True),
        sa.Column('skill_vector', sa.JSON(), nullable=True),
        sa.Column('predicted_labels', sa.JSON(), nullable=True),
        sa.Column('latency_ms', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['job_description_id'], ['job_descriptions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_scores_resume_id', 'scores', ['resume_id'])
    op.create_index('ix_scores_job_description_id', 'scores', ['job_description_id'])

    # 6. red_flags
    op.create_table(
        'red_flags',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('resume_id', sa.String(length=36), nullable=False),
        sa.Column('score_id', sa.String(length=36), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('severity', sa.String(length=20), nullable=False),
        sa.Column('flag_message', sa.String(length=255), nullable=False),
        sa.Column('context_snippet', sa.Text(), nullable=True),
        sa.Column('recommendation', sa.Text(), nullable=False),
        sa.Column('penalty_points', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['score_id'], ['scores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_red_flags_resume_id', 'red_flags', ['resume_id'])
    op.create_index('ix_red_flags_category', 'red_flags', ['category'])

def downgrade():
    op.drop_table('red_flags')
    op.drop_table('scores')
    op.drop_table('resume_skills')
    op.drop_table('skills')
    op.drop_table('job_descriptions')
    op.drop_table('resumes')
