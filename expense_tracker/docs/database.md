# Database Design

## Entities
- `User`
- `Category`
- `Expense`
- `Income`
- `Budget`
- `Notification`

## Relationships
- One user has many categories, expenses, incomes, budgets, and notifications.
- Each expense belongs to one category and one user.
- Each budget can be monthly or category-specific.
