from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, Income, Expense, Category
from app.forms import LoginForm, RegistrationForm, IncomeForm, ExpenseForm, CategoryForm


@app.route('/')
def index():
    return render_template('index.html', current_user = current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)#, remember=form.remember_me.data)
        return redirect(url_for('dashboard'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    incomes = Income.query.join(Category).add_columns().filter_by(user_id=current_user.id).all()
    expenses = Expense.query.join(Category).filter_by(user_id=current_user.id).all()
    income_total = sum(income.amount for income in incomes)
    expense_total = sum(expense.amount for expense in expenses)
    for income in incomes:
        print(f"Income ID: {income.income_id}")
        print(f"User ID: {income.user_id}")
        print(f"Amount: {income.amount}")
        print(f"Description: {income.description}")
        print(f"Date: {income.date}")
        print(f"Category ID: {income.category_id}")
        print(f"Category Name: {income.category.name}")
        print("----------------------------------------")
    print(income_total)
    return render_template('dashboard.html', incomes=incomes, expenses=expenses, total_income=income_total, total_expenses=expense_total)


@app.route('/income/add', methods=['GET', 'POST'])
@login_required
def add_income():
    form = IncomeForm()
    form.category.choices = [(c.category_id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():
        print(form.category.data)
        income = Income(user_id=current_user.id, amount=form.amount.data, description=form.description.data,
                        date=form.date.data, category_id=form.category.data)
        db.session.add(income)
        db.session.commit()
        flash('Your income has been added successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('add_income.html', title='Add Income', form=form)


@app.route('/income/<int:income_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_income(income_id):
    income = Income.query.get_or_404(income_id)
    if income.user_id != current_user.id:
        return redirect(url_for('index'))
    form = IncomeForm(obj=income)
    if form.validate_on_submit():
        income.amount = form.amount.data
        income.description = form.description.data
        income.date = form.date.data
        income.category_id = form.category.data.category_id
        db.session.commit()
        flash('Your income has been updated successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_income.html', title='Edit Income', form=form)


@app.route('/income/<int:income_id>/delete', methods=['POST'])
@login_required
def delete_income(income_id):
    income = Income.query.get_or_404(income_id)
    if income.user_id != current_user.id:
        return redirect(url_for('index'))
    db.session.delete(income)
    db.session.commit()
    flash('Your income has been deleted successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/expense/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    form.category.choices = Category.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        expense = Expense(user_id=current_user.id, amount=form.amount.data, description=form.description.data,
                        date=form.date.data, category_id=form.category.data.category_id)
        db.session.add(expense)
        db.session.commit()
        flash('Your expense has been added successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('add_expense.html', title='Add Expense', form=form)


@app.route('/expense/<int:expense_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        return redirect(url_for('index'))
    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.description = form.description.data
        expense.date = form.date.data
        expense.category_id = form.category.data.category_id
        db.session.commit()
        flash('Your expense has been updated successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_expense.html', title='Edit Expense', form=form)


@app.route('/expense/<int:expense_id>/delete', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        return redirect(url_for('index'))
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/category/add', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            is_income=form.is_income.data,
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully', 'success')
        return redirect(url_for('view_categories'))

    return render_template('add_category.html', title='Add Category', form=form)


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)

    if category.user_id != current_user.id:
        abort(403)

    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        category.is_income = form.is_income.data
        db.session.commit()
        flash('Category updated successfully', 'success')
        return redirect(url_for('view_categories'))

    form.name.data = category.name
    form.is_income.data = category.is_income

    return render_template('edit_category.html', title='Edit Category', form=form)


@app.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    if category.user_id != current_user.id:
        abort(403)

    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully', 'success')
    return redirect(url_for('view_categories'))

@app.route('/transactions')
@login_required
def view_transactions():
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    transactions = incomes + expenses
    transactions.sort(key=lambda x: x.date, reverse=True)
    return render_template('transactions.html', transactions=transactions)

@app.route('/categories')
@login_required
def view_categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories.html', categories=categories)
