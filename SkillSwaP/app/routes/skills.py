from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.skill import Skill
from app.forms import SkillForm

skills_bp = Blueprint('skills_bp', __name__)

# view all user skills
@skills_bp.route('/skills')
@login_required
def skills():
    return render_template('skills/skills.html', skills = current_user.skills )


# Add a skill
@skills_bp.route('/skills/add', methods=['POST', "GET"])
@login_required
def add_skill():
    form = SkillForm()
    if form.validate_on_submit():
        new_skill = Skill(
            name = form.name.data,
            category = form.category.data,
            description = form.description.data,
            skill_type = form.skill_type.data,
            user_id = current_user.id
        )
        db.session.add(new_skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('skills_bp.skills'))
    return render_template('skills/add_skill.html', form = form)


# update skill route
@skills_bp.route('/skills/update/<int:skill_id>', methods=['POST', 'GET'])
@login_required
def update_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.user_id != current_user.id:
        flash('Unauthorized!', 'danger')
        return redirect(url_for('skills_bp.skills'))
    
    form = SkillForm(obj=skill)
    if form.validate_on_submit():
        skill.name = form.name.data
        skill.category = form.category.data
        skill.description = form.description.data
        skill.skill_type = form.skill_type.data
        db.session.commit()
        flash('Skill updated!', 'success')
        return redirect(url_for('skills_bp.skills'))
    return render_template('skills/update_skill.html', form = form, skill = skill)


# delete skill route
@skills_bp.route('/skills/delete/<int:skill_id>', methods=['POST'])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.user_id != current_user.id:
        flash('Unauthorized!', 'danger')
        return redirect(url_for('skills_bp.skills'))

    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted!', 'info')
    return redirect(url_for('skills_bp.skills'))