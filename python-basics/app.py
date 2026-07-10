import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


APP_TITLE = "Inspire Steam POS"
CURRENCY = "$"


@dataclass
class Product:
    code: str
    name: str
    category: str
    price: float
    stock: int


class POS:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1180x760")
        self.root.minsize(980, 640)

        self.colors = {
            "bg": "#eef3f7",
            "panel": "#ffffff",
            "panel_alt": "#f8fafc",
            "text": "#17212f",
            "muted": "#617083",
            "border": "#d9e2ec",
            "accent": "#146c75",
            "accent_dark": "#0f5158",
            "success": "#1f7a4d",
            "danger": "#ba2f42",
            "warning": "#b77700",
            "header": "#0f2630",
        }

        self.products = self.load_products()
        self.cart = {}
        self.completed_sales = 0
        self.session_revenue = 0.0
        self.last_receipt_text = ""
        self.current_receipt_no = self.new_receipt_number()

        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All categories")
        self.code_var = tk.StringVar()
        self.qty_var = tk.StringVar(value="1")
        self.customer_var = tk.StringVar(value="Walk-in customer")
        self.payment_var = tk.StringVar(value="Cash")
        self.discount_var = tk.StringVar(value="0")
        self.tax_var = tk.StringVar(value="0")
        self.cash_var = tk.StringVar(value="0.00")
        self.status_var = tk.StringVar(value="Ready for checkout")

        self.subtotal_var = tk.StringVar(value=self.money(0))
        self.discount_amount_var = tk.StringVar(value=self.money(0))
        self.tax_amount_var = tk.StringVar(value=self.money(0))
        self.due_var = tk.StringVar(value=self.money(0))
        self.change_var = tk.StringVar(value=self.money(0))
        self.items_count_var = tk.StringVar(value="0 items")
        self.sales_count_var = tk.StringVar(value="0 sales")
        self.revenue_var = tk.StringVar(value=self.money(0))

        self.configure_styles()
        self.create_menu()
        self.create_widgets()
        self.bind_shortcuts()

        for var in (self.discount_var, self.tax_var, self.cash_var, self.payment_var):
            var.trace_add("write", lambda *_: self.update_totals())

        self.refresh_product_table()
        self.refresh_cart_table()
        self.update_totals()
        self.code_entry.focus_set()

    def load_products(self):
        products = [
            Product("1001", "Milk 1L", "Dairy", 1.50, 42),
            Product("1002", "Bread", "Bakery", 1.00, 37),
            Product("1003", "Sugar 1Kg", "Pantry", 2.20, 25),
            Product("1004", "Rice 1Kg", "Pantry", 1.80, 33),
            Product("1005", "Soap", "Home Care", 0.80, 18),
            Product("1006", "Eggs 12 Pack", "Dairy", 3.40, 16),
            Product("1007", "Cooking Oil 1L", "Pantry", 4.50, 20),
            Product("1008", "Tomatoes 1Kg", "Fresh", 2.10, 28),
            Product("1009", "Bananas 1Kg", "Fresh", 1.70, 31),
            Product("1010", "Chicken Breast", "Meat", 6.90, 14),
            Product("1011", "Toothpaste", "Personal Care", 2.60, 22),
            Product("1012", "Laundry Powder", "Home Care", 5.20, 12),
            Product("1013", "Bottled Water", "Drinks", 0.70, 56),
            Product("1014", "Orange Juice", "Drinks", 2.90, 17),
            Product("1015", "Coffee 250g", "Pantry", 4.80, 11),
            Product("1016", "Yoghurt Cup", "Dairy", 0.95, 30),
            Product("1017", "Pasta 500g", "Pantry", 1.35, 24),
            Product("1018", "Granola Bars", "Snacks", 2.75, 19),
        ]
        return {product.code: product for product in products}

    def configure_styles(self):
        self.root.configure(bg=self.colors["bg"])
        self.root.option_add("*Font", "{Segoe UI} 10")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(".", font=("Segoe UI", 10))
        style.configure("App.TFrame", background=self.colors["bg"])
        style.configure("Panel.TFrame", background=self.colors["panel"], relief="flat")
        style.configure("Header.TFrame", background=self.colors["header"])
        style.configure("PanelAlt.TFrame", background=self.colors["panel_alt"])

        style.configure(
            "Title.TLabel",
            background=self.colors["header"],
            foreground="#ffffff",
            font=("Segoe UI", 20, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=self.colors["header"],
            foreground="#b8c7d2",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Logo.TLabel",
            background=self.colors["accent"],
            foreground="#ffffff",
            font=("Segoe UI", 15, "bold"),
            padding=(12, 8),
        )
        style.configure(
            "PanelTitle.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["text"],
            font=("Segoe UI", 13, "bold"),
        )
        style.configure(
            "PanelSubtle.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["muted"],
            font=("Segoe UI", 9),
        )
        style.configure(
            "MetricLabel.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["muted"],
            font=("Segoe UI", 9),
        )
        style.configure(
            "MetricValue.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["text"],
            font=("Segoe UI", 12, "bold"),
        )
        style.configure(
            "DueValue.TLabel",
            background=self.colors["panel"],
            foreground=self.colors["accent"],
            font=("Segoe UI", 18, "bold"),
        )
        style.configure("TLabel", background=self.colors["panel"], foreground=self.colors["text"])
        style.configure("TEntry", padding=(8, 6), relief="flat")
        style.configure("TCombobox", padding=(8, 6), relief="flat")
        style.configure("TSpinbox", arrowsize=14, padding=(8, 6))
        style.configure("TButton", padding=(12, 8), borderwidth=0)
        style.configure(
            "Accent.TButton",
            background=self.colors["accent"],
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Accent.TButton",
            background=[("active", self.colors["accent_dark"]), ("disabled", "#93a6aa")],
            foreground=[("disabled", "#eef3f7")],
        )
        style.configure(
            "Danger.TButton",
            background=self.colors["danger"],
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Danger.TButton", background=[("active", "#932436"), ("disabled", "#d8a1aa")])
        style.configure(
            "Success.TButton",
            background=self.colors["success"],
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Success.TButton", background=[("active", "#155d39"), ("disabled", "#93b9a5")])
        style.configure("Ghost.TButton", background=self.colors["panel_alt"], foreground=self.colors["text"])
        style.map("Ghost.TButton", background=[("active", "#e6edf4")])
        style.configure(
            "Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground=self.colors["text"],
            rowheight=32,
            borderwidth=0,
            relief="flat",
        )
        style.configure(
            "Treeview.Heading",
            background="#e8eef4",
            foreground=self.colors["text"],
            font=("Segoe UI", 9, "bold"),
            padding=(8, 8),
            relief="flat",
        )
        style.map("Treeview", background=[("selected", self.colors["accent"])], foreground=[("selected", "#ffffff")])
        style.configure("Status.TLabel", background=self.colors["bg"], foreground=self.colors["muted"])

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New sale", command=self.reset_sale)
        file_menu.add_command(label="Save receipt", command=self.save_receipt)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        sale_menu = tk.Menu(menubar, tearoff=0)
        sale_menu.add_command(label="Add item", command=self.add_to_cart)
        sale_menu.add_command(label="Complete sale", command=self.complete_sale)
        sale_menu.add_command(label="Remove selected", command=self.remove_selected_item)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Sale", menu=sale_menu)
        self.root.config(menu=menubar)

    def create_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        header = ttk.Frame(self.root, style="Header.TFrame", padding=(22, 16))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(1, weight=1)

        ttk.Label(header, text="IS", style="Logo.TLabel").grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 14))
        ttk.Label(header, text=APP_TITLE, style="Title.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Label(header, text="Supermarket checkout", style="Subtitle.TLabel").grid(row=1, column=1, sticky="w")

        stats = ttk.Frame(header, style="Header.TFrame")
        stats.grid(row=0, column=2, rowspan=2, sticky="e")
        self.create_header_metric(stats, "Sales", self.sales_count_var, 0)
        self.create_header_metric(stats, "Revenue", self.revenue_var, 1)

        workspace = ttk.Frame(self.root, style="App.TFrame", padding=(18, 16, 18, 10))
        workspace.grid(row=1, column=0, sticky="nsew")
        workspace.columnconfigure(0, weight=4, minsize=330)
        workspace.columnconfigure(1, weight=5, minsize=390)
        workspace.columnconfigure(2, weight=3, minsize=280)
        workspace.rowconfigure(0, weight=1)

        self.create_catalog_panel(workspace)
        self.create_cart_panel(workspace)
        self.create_summary_panel(workspace)

        status = ttk.Frame(self.root, style="App.TFrame", padding=(18, 0, 18, 12))
        status.grid(row=2, column=0, sticky="ew")
        status.columnconfigure(0, weight=1)
        ttk.Label(status, textvariable=self.status_var, style="Status.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(status, textvariable=self.items_count_var, style="Status.TLabel").grid(row=0, column=1, sticky="e")

    def create_header_metric(self, parent, label, variable, column):
        box = ttk.Frame(parent, style="Header.TFrame", padding=(18, 0, 0, 0))
        box.grid(row=0, column=column, rowspan=2, sticky="e")
        tk.Label(
            box,
            text=label.upper(),
            bg=self.colors["header"],
            fg="#8fa4b1",
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="e")
        tk.Label(
            box,
            textvariable=variable,
            bg=self.colors["header"],
            fg="#ffffff",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="e")

    def create_catalog_panel(self, parent):
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(7, weight=1)

        ttk.Label(panel, text="Product Catalogue", style="PanelTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(panel, text="Inventory and pricing", style="PanelSubtle.TLabel").grid(
            row=1, column=0, sticky="w", pady=(2, 14)
        )

        entry_grid = ttk.Frame(panel, style="Panel.TFrame")
        entry_grid.grid(row=2, column=0, sticky="ew")
        entry_grid.columnconfigure(0, weight=1)
        entry_grid.columnconfigure(1, weight=0)
        entry_grid.columnconfigure(2, weight=0)

        ttk.Label(entry_grid, text="Code").grid(row=0, column=0, sticky="w")
        ttk.Label(entry_grid, text="Qty").grid(row=0, column=1, sticky="w", padx=(10, 0))
        self.code_entry = ttk.Entry(entry_grid, textvariable=self.code_var)
        self.code_entry.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        self.qty_entry = ttk.Spinbox(entry_grid, from_=1, to=999, textvariable=self.qty_var, width=7)
        self.qty_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(4, 0))
        self.code_entry.bind("<Return>", lambda _event: self.add_to_cart())
        self.qty_entry.bind("<Return>", lambda _event: self.add_to_cart())
        ttk.Button(entry_grid, text="Add", style="Accent.TButton", command=self.add_to_cart).grid(
            row=1, column=2, sticky="ew", padx=(10, 0), pady=(4, 0)
        )

        filters = ttk.Frame(panel, style="Panel.TFrame")
        filters.grid(row=3, column=0, sticky="ew", pady=(16, 8))
        filters.columnconfigure(0, weight=1)
        filters.columnconfigure(1, weight=0)
        ttk.Entry(filters, textvariable=self.search_var).grid(row=0, column=0, sticky="ew")

        categories = ["All categories"] + sorted({product.category for product in self.products.values()})
        self.category_combo = ttk.Combobox(
            filters,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            width=17,
        )
        self.category_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0))

        self.product_tree = ttk.Treeview(
            panel,
            columns=("code", "name", "category", "price", "available"),
            show="headings",
            selectmode="browse",
            height=12,
        )
        self.product_tree.grid(row=7, column=0, sticky="nsew", pady=(8, 0))
        self.product_tree.heading("code", text="Code")
        self.product_tree.heading("name", text="Product")
        self.product_tree.heading("category", text="Category")
        self.product_tree.heading("price", text="Price")
        self.product_tree.heading("available", text="Available")
        self.product_tree.column("code", width=72, anchor=tk.CENTER, stretch=False)
        self.product_tree.column("name", width=150, anchor=tk.W)
        self.product_tree.column("category", width=110, anchor=tk.W)
        self.product_tree.column("price", width=82, anchor=tk.E, stretch=False)
        self.product_tree.column("available", width=82, anchor=tk.CENTER, stretch=False)
        self.product_tree.tag_configure("low", background="#fff6db")
        self.product_tree.tag_configure("out", background="#ffe7eb")

        product_scroll = ttk.Scrollbar(panel, orient=tk.VERTICAL, command=self.product_tree.yview)
        product_scroll.grid(row=7, column=1, sticky="ns", pady=(8, 0))
        self.product_tree.configure(yscrollcommand=product_scroll.set)

        self.search_var.trace_add("write", lambda *_: self.refresh_product_table())
        self.category_combo.bind("<<ComboboxSelected>>", lambda _event: self.refresh_product_table())
        self.product_tree.bind("<Double-1>", lambda _event: self.add_selected_product())
        self.product_tree.bind("<<TreeviewSelect>>", self.copy_selected_product_code)

    def create_cart_panel(self, parent):
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        panel.grid(row=0, column=1, sticky="nsew", padx=12)
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(4, weight=1)

        title_row = ttk.Frame(panel, style="Panel.TFrame")
        title_row.grid(row=0, column=0, sticky="ew")
        title_row.columnconfigure(0, weight=1)
        ttk.Label(title_row, text="Current Cart", style="PanelTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(title_row, text="New sale", style="Ghost.TButton", command=self.reset_sale).grid(
            row=0, column=1, sticky="e"
        )
        ttk.Label(panel, text="Open transaction", style="PanelSubtle.TLabel").grid(
            row=1, column=0, sticky="w", pady=(2, 14)
        )

        controls = ttk.Frame(panel, style="Panel.TFrame")
        controls.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        controls.columnconfigure(5, weight=1)
        self.minus_button = ttk.Button(controls, text="-", style="Ghost.TButton", width=4, command=lambda: self.adjust_selected_quantity(-1))
        self.minus_button.grid(row=0, column=0, padx=(0, 8))
        self.plus_button = ttk.Button(controls, text="+", style="Ghost.TButton", width=4, command=lambda: self.adjust_selected_quantity(1))
        self.plus_button.grid(row=0, column=1, padx=(0, 8))
        self.remove_button = ttk.Button(controls, text="Remove", style="Danger.TButton", command=self.remove_selected_item)
        self.remove_button.grid(row=0, column=2, padx=(0, 8))
        self.clear_button = ttk.Button(controls, text="Clear", style="Ghost.TButton", command=self.clear_cart)
        self.clear_button.grid(row=0, column=3, padx=(0, 8))

        self.cart_tree = ttk.Treeview(
            panel,
            columns=("code", "name", "price", "qty", "total"),
            show="headings",
            selectmode="browse",
            height=13,
        )
        self.cart_tree.grid(row=4, column=0, sticky="nsew")
        self.cart_tree.heading("code", text="Code")
        self.cart_tree.heading("name", text="Item")
        self.cart_tree.heading("price", text="Unit")
        self.cart_tree.heading("qty", text="Qty")
        self.cart_tree.heading("total", text="Total")
        self.cart_tree.column("code", width=70, anchor=tk.CENTER, stretch=False)
        self.cart_tree.column("name", width=190, anchor=tk.W)
        self.cart_tree.column("price", width=80, anchor=tk.E, stretch=False)
        self.cart_tree.column("qty", width=55, anchor=tk.CENTER, stretch=False)
        self.cart_tree.column("total", width=90, anchor=tk.E, stretch=False)
        self.cart_tree.bind("<Delete>", lambda _event: self.remove_selected_item())

        cart_scroll = ttk.Scrollbar(panel, orient=tk.VERTICAL, command=self.cart_tree.yview)
        cart_scroll.grid(row=4, column=1, sticky="ns")
        self.cart_tree.configure(yscrollcommand=cart_scroll.set)

        totals_strip = ttk.Frame(panel, style="PanelAlt.TFrame", padding=(14, 12))
        totals_strip.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(14, 0))
        totals_strip.columnconfigure(0, weight=1)
        tk.Label(
            totals_strip,
            text="Amount Due",
            bg=self.colors["panel_alt"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            totals_strip,
            textvariable=self.due_var,
            bg=self.colors["panel_alt"],
            fg=self.colors["accent"],
            font=("Segoe UI", 22, "bold"),
        ).grid(row=1, column=0, sticky="w")
        tk.Label(
            totals_strip,
            text="Change",
            bg=self.colors["panel_alt"],
            fg=self.colors["muted"],
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=1, sticky="e", padx=(20, 0))
        tk.Label(
            totals_strip,
            textvariable=self.change_var,
            bg=self.colors["panel_alt"],
            fg=self.colors["success"],
            font=("Segoe UI", 16, "bold"),
        ).grid(row=1, column=1, sticky="e", padx=(20, 0))

    def create_summary_panel(self, parent):
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        panel.grid(row=0, column=2, sticky="nsew", padx=(12, 0))
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(15, weight=1)

        ttk.Label(panel, text="Payment", style="PanelTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(panel, text="Tender and receipt", style="PanelSubtle.TLabel").grid(
            row=1, column=0, sticky="w", pady=(2, 14)
        )

        form = ttk.Frame(panel, style="Panel.TFrame")
        form.grid(row=2, column=0, sticky="ew")
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Customer").grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Entry(form, textvariable=self.customer_var).grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 10))

        ttk.Label(form, text="Payment method").grid(row=2, column=0, sticky="w")
        ttk.Label(form, text="Cash paid").grid(row=2, column=1, sticky="w", padx=(10, 0))
        ttk.Combobox(
            form,
            textvariable=self.payment_var,
            values=("Cash", "Card", "Mobile money", "Voucher"),
            state="readonly",
        ).grid(row=3, column=0, sticky="ew", pady=(4, 10))
        cash_entry = ttk.Entry(form, textvariable=self.cash_var)
        cash_entry.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=(4, 10))
        self.cash_entry = cash_entry

        ttk.Label(form, text="Discount %").grid(row=4, column=0, sticky="w")
        ttk.Label(form, text="Tax %").grid(row=4, column=1, sticky="w", padx=(10, 0))
        ttk.Entry(form, textvariable=self.discount_var).grid(row=5, column=0, sticky="ew", pady=(4, 0))
        ttk.Entry(form, textvariable=self.tax_var).grid(row=5, column=1, sticky="ew", padx=(10, 0), pady=(4, 0))

        summary = ttk.Frame(panel, style="Panel.TFrame")
        summary.grid(row=3, column=0, sticky="ew", pady=(18, 10))
        summary.columnconfigure(1, weight=1)
        self.create_amount_row(summary, "Subtotal", self.subtotal_var, 0)
        self.create_amount_row(summary, "Discount", self.discount_amount_var, 1)
        self.create_amount_row(summary, "Tax", self.tax_amount_var, 2)
        ttk.Separator(summary).grid(row=3, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Label(summary, text="Total Due", style="MetricLabel.TLabel").grid(row=4, column=0, sticky="w")
        ttk.Label(summary, textvariable=self.due_var, style="DueValue.TLabel").grid(row=4, column=1, sticky="e")

        button_row = ttk.Frame(panel, style="Panel.TFrame")
        button_row.grid(row=4, column=0, sticky="ew", pady=(4, 14))
        button_row.columnconfigure(0, weight=1)
        button_row.columnconfigure(1, weight=1)
        self.complete_button = ttk.Button(
            button_row,
            text="Complete sale",
            style="Success.TButton",
            command=self.complete_sale,
        )
        self.complete_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.save_button = ttk.Button(
            button_row,
            text="Save receipt",
            style="Accent.TButton",
            command=self.save_receipt,
        )
        self.save_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        ttk.Label(panel, text="Receipt Preview", style="PanelTitle.TLabel").grid(row=5, column=0, sticky="w")
        receipt_frame = ttk.Frame(panel, style="Panel.TFrame")
        receipt_frame.grid(row=15, column=0, sticky="nsew", pady=(8, 0))
        receipt_frame.columnconfigure(0, weight=1)
        receipt_frame.rowconfigure(0, weight=1)
        self.receipt_text = tk.Text(
            receipt_frame,
            height=12,
            wrap="word",
            borderwidth=0,
            bg="#f8fafc",
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            font=("Consolas", 9),
            padx=10,
            pady=10,
        )
        self.receipt_text.grid(row=0, column=0, sticky="nsew")
        receipt_scroll = ttk.Scrollbar(receipt_frame, orient=tk.VERTICAL, command=self.receipt_text.yview)
        receipt_scroll.grid(row=0, column=1, sticky="ns")
        self.receipt_text.configure(yscrollcommand=receipt_scroll.set, state="disabled")

    def create_amount_row(self, parent, label, variable, row):
        ttk.Label(parent, text=label, style="MetricLabel.TLabel").grid(row=row, column=0, sticky="w", pady=3)
        ttk.Label(parent, textvariable=variable, style="MetricValue.TLabel").grid(row=row, column=1, sticky="e", pady=3)

    def bind_shortcuts(self):
        self.root.bind("<Control-l>", lambda _event: self.focus_lookup())
        self.root.bind("<Control-L>", lambda _event: self.focus_lookup())
        self.root.bind("<Control-s>", lambda _event: self.save_receipt())
        self.root.bind("<Control-S>", lambda _event: self.save_receipt())
        self.root.bind("<F2>", lambda _event: self.focus_cash())
        self.root.bind("<F5>", lambda _event: self.reset_sale())

    def focus_lookup(self):
        self.code_entry.focus_set()
        self.code_entry.select_range(0, tk.END)

    def focus_cash(self):
        self.cash_entry.focus_set()
        self.cash_entry.select_range(0, tk.END)

    def copy_selected_product_code(self, _event=None):
        selected = self.product_tree.selection()
        if not selected:
            return
        code = self.product_tree.item(selected[0], "values")[0]
        self.code_var.set(code)

    def add_selected_product(self):
        selected = self.product_tree.selection()
        if not selected:
            self.set_status("Select a product first")
            return
        code = self.product_tree.item(selected[0], "values")[0]
        self.code_var.set(code)
        self.add_to_cart()

    def add_to_cart(self):
        code = self.code_var.get().strip()
        if not code:
            selected = self.product_tree.selection()
            if selected:
                code = self.product_tree.item(selected[0], "values")[0]

        if not code:
            self.set_status("Enter a product code")
            return

        product = self.products.get(code)
        if product is None:
            messagebox.showerror("Product not found", f"No product uses code {code}.")
            self.set_status("Product not found")
            return

        try:
            qty = int(self.qty_var.get())
        except ValueError:
            messagebox.showerror("Invalid quantity", "Quantity must be a whole number.")
            self.qty_var.set("1")
            return

        if qty < 1:
            messagebox.showerror("Invalid quantity", "Quantity must be at least 1.")
            self.qty_var.set("1")
            return

        current_qty = self.cart.get(code, 0)
        if current_qty + qty > product.stock:
            messagebox.showwarning(
                "Not enough stock",
                f"Only {product.stock - current_qty} available for {product.name}.",
            )
            return

        self.cart[code] = current_qty + qty
        self.code_var.set("")
        self.qty_var.set("1")
        self.last_receipt_text = ""
        self.refresh_cart_table()
        self.refresh_product_table()
        self.update_totals()
        self.set_status(f"Added {qty} x {product.name}")
        self.code_entry.focus_set()

    def refresh_product_table(self):
        if not hasattr(self, "product_tree"):
            return

        query = self.search_var.get().strip().lower()
        category = self.category_var.get()
        self.product_tree.delete(*self.product_tree.get_children())

        for product in sorted(self.products.values(), key=lambda item: (item.category, item.name)):
            if category != "All categories" and product.category != category:
                continue
            searchable = f"{product.code} {product.name} {product.category}".lower()
            if query and query not in searchable:
                continue

            available = product.stock - self.cart.get(product.code, 0)
            tags = ()
            if available <= 0:
                tags = ("out",)
            elif available <= 5:
                tags = ("low",)

            self.product_tree.insert(
                "",
                tk.END,
                values=(product.code, product.name, product.category, self.money(product.price), available),
                tags=tags,
            )

    def refresh_cart_table(self):
        if not hasattr(self, "cart_tree"):
            return

        self.cart_tree.delete(*self.cart_tree.get_children())
        for code, qty in self.cart.items():
            product = self.products[code]
            line_total = product.price * qty
            self.cart_tree.insert(
                "",
                tk.END,
                values=(code, product.name, self.money(product.price), qty, self.money(line_total)),
            )

        item_total = sum(self.cart.values())
        label = "item" if item_total == 1 else "items"
        self.items_count_var.set(f"{item_total} {label} in cart")
        self.update_action_states()

    def selected_cart_code(self):
        selected = self.cart_tree.selection()
        if not selected:
            return None
        return self.cart_tree.item(selected[0], "values")[0]

    def adjust_selected_quantity(self, amount):
        code = self.selected_cart_code()
        if code is None:
            self.set_status("Select a cart item first")
            return

        product = self.products[code]
        new_qty = self.cart[code] + amount
        if new_qty <= 0:
            del self.cart[code]
            self.set_status(f"Removed {product.name}")
        elif new_qty > product.stock:
            messagebox.showwarning("Not enough stock", f"Only {product.stock} available for {product.name}.")
            return
        else:
            self.cart[code] = new_qty
            self.set_status(f"Updated {product.name} quantity to {new_qty}")

        self.last_receipt_text = ""
        self.refresh_cart_table()
        self.refresh_product_table()
        self.update_totals()

    def remove_selected_item(self):
        if not hasattr(self, "cart_tree"):
            return

        code = self.selected_cart_code()
        if code is None:
            return

        product_name = self.products[code].name
        del self.cart[code]
        self.last_receipt_text = ""
        self.refresh_cart_table()
        self.refresh_product_table()
        self.update_totals()
        self.set_status(f"Removed {product_name}")

    def clear_cart(self):
        if not self.cart:
            return
        if not messagebox.askyesno("Clear cart", "Remove every item from this cart?"):
            return
        self.cart.clear()
        self.last_receipt_text = ""
        self.refresh_cart_table()
        self.refresh_product_table()
        self.update_totals()
        self.set_status("Cart cleared")

    def reset_sale(self):
        if self.cart and not messagebox.askyesno("New sale", "Discard the current cart and start a new sale?"):
            return
        self.cart.clear()
        self.current_receipt_no = self.new_receipt_number()
        self.code_var.set("")
        self.qty_var.set("1")
        self.customer_var.set("Walk-in customer")
        self.payment_var.set("Cash")
        self.discount_var.set("0")
        self.tax_var.set("0")
        self.cash_var.set("0.00")
        self.last_receipt_text = ""
        self.refresh_cart_table()
        self.refresh_product_table()
        self.update_totals()
        self.set_status("New sale ready")
        self.code_entry.focus_set()

    def update_totals(self):
        subtotal = sum(self.products[code].price * qty for code, qty in self.cart.items())
        discount_rate = self.safe_float(self.discount_var.get())
        tax_rate = self.safe_float(self.tax_var.get())
        cash_paid = self.safe_float(self.cash_var.get())

        discount_rate = min(max(discount_rate, 0), 100)
        tax_rate = max(tax_rate, 0)

        discount_amount = subtotal * (discount_rate / 100)
        taxable_total = max(subtotal - discount_amount, 0)
        tax_amount = taxable_total * (tax_rate / 100)
        due = taxable_total + tax_amount

        payment_method = self.payment_var.get()
        if payment_method != "Cash" and cash_paid <= 0:
            cash_paid = due
        change = max(cash_paid - due, 0)

        self.subtotal_var.set(self.money(subtotal))
        self.discount_amount_var.set(f"-{self.money(discount_amount)}")
        self.tax_amount_var.set(self.money(tax_amount))
        self.due_var.set(self.money(due))
        self.change_var.set(self.money(change))
        self.update_receipt_preview()
        self.update_action_states()

    def update_action_states(self):
        has_cart = bool(self.cart)
        has_receipt = has_cart or bool(self.last_receipt_text)
        state_cart = tk.NORMAL if has_cart else tk.DISABLED
        state_receipt = tk.NORMAL if has_receipt else tk.DISABLED

        for button_name in ("minus_button", "plus_button", "remove_button", "clear_button", "complete_button"):
            button = getattr(self, button_name, None)
            if button is not None:
                button.configure(state=state_cart)

        if hasattr(self, "save_button"):
            self.save_button.configure(state=state_receipt)

    def validate_sale_inputs(self):
        try:
            discount_rate = float(self.discount_var.get() or 0)
            tax_rate = float(self.tax_var.get() or 0)
            cash_paid = float(self.cash_var.get() or 0)
        except ValueError:
            messagebox.showerror("Invalid payment details", "Discount, tax, and cash paid must be numbers.")
            return None

        if discount_rate < 0 or discount_rate > 100:
            messagebox.showerror("Invalid discount", "Discount must be between 0 and 100 percent.")
            return None
        if tax_rate < 0:
            messagebox.showerror("Invalid tax", "Tax cannot be negative.")
            return None
        if cash_paid < 0:
            messagebox.showerror("Invalid cash paid", "Cash paid cannot be negative.")
            return None

        subtotal = sum(self.products[code].price * qty for code, qty in self.cart.items())
        discount_amount = subtotal * (discount_rate / 100)
        taxable_total = max(subtotal - discount_amount, 0)
        tax_amount = taxable_total * (tax_rate / 100)
        due = taxable_total + tax_amount

        payment_method = self.payment_var.get()
        if payment_method == "Cash" and cash_paid < due:
            messagebox.showwarning("Payment short", f"Cash paid is short by {self.money(due - cash_paid)}.")
            return None
        if payment_method != "Cash" and cash_paid <= 0:
            cash_paid = due

        return {
            "subtotal": subtotal,
            "discount_rate": discount_rate,
            "discount_amount": discount_amount,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "due": due,
            "cash_paid": cash_paid,
            "change": max(cash_paid - due, 0),
        }

    def complete_sale(self):
        if not self.cart:
            messagebox.showinfo("Empty cart", "Add products before completing a sale.")
            return

        totals = self.validate_sale_inputs()
        if totals is None:
            return

        receipt = self.build_receipt(totals, completed=True)
        for code, qty in self.cart.items():
            self.products[code].stock -= qty

        self.completed_sales += 1
        self.session_revenue += totals["due"]
        self.sales_count_var.set(f"{self.completed_sales} sales")
        self.revenue_var.set(self.money(self.session_revenue))
        self.last_receipt_text = receipt
        self.cart.clear()
        self.current_receipt_no = self.new_receipt_number()
        self.cash_var.set("0.00")
        self.refresh_cart_table()
        self.refresh_product_table()
        self.update_totals()
        self.show_receipt_text(receipt)
        self.set_status(f"Sale completed. Change: {self.money(totals['change'])}")
        messagebox.showinfo("Sale complete", f"Payment accepted.\nChange: {self.money(totals['change'])}")

    def update_receipt_preview(self):
        if not hasattr(self, "receipt_text"):
            return

        if self.cart:
            receipt = self.build_receipt(self.current_totals(), completed=False)
        elif self.last_receipt_text:
            receipt = self.last_receipt_text
        else:
            receipt = "No active sale."
        self.show_receipt_text(receipt)

    def show_receipt_text(self, receipt):
        self.receipt_text.configure(state="normal")
        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert(tk.END, receipt)
        self.receipt_text.configure(state="disabled")

    def current_totals(self):
        subtotal = sum(self.products[code].price * qty for code, qty in self.cart.items())
        discount_rate = min(max(self.safe_float(self.discount_var.get()), 0), 100)
        tax_rate = max(self.safe_float(self.tax_var.get()), 0)
        cash_paid = max(self.safe_float(self.cash_var.get()), 0)
        discount_amount = subtotal * (discount_rate / 100)
        taxable_total = max(subtotal - discount_amount, 0)
        tax_amount = taxable_total * (tax_rate / 100)
        due = taxable_total + tax_amount
        if self.payment_var.get() != "Cash" and cash_paid <= 0:
            cash_paid = due
        return {
            "subtotal": subtotal,
            "discount_rate": discount_rate,
            "discount_amount": discount_amount,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "due": due,
            "cash_paid": cash_paid,
            "change": max(cash_paid - due, 0),
        }

    def build_receipt(self, totals, completed=False):
        customer = self.customer_var.get().strip() or "Walk-in customer"
        status = "PAID" if completed else "DRAFT"
        lines = [
            "INSPIRE STEAM SUPERMARKET",
            "Modern POS Receipt",
            f"Receipt: {self.current_receipt_no}",
            f"Status: {status}",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"Customer: {customer}",
            f"Payment: {self.payment_var.get()}",
            "-" * 42,
            f"{'Item':<22}{'Qty':>5}{'Total':>13}",
            "-" * 42,
        ]

        if self.cart:
            for code, qty in self.cart.items():
                product = self.products[code]
                name = product.name[:21]
                lines.append(f"{name:<22}{qty:>5}{self.money(product.price * qty):>13}")
        else:
            lines.append("No items")

        lines.extend(
            [
                "-" * 42,
                f"{'Subtotal':<27}{self.money(totals['subtotal']):>15}",
                f"{'Discount':<27}{('-' + self.money(totals['discount_amount'])):>15}",
                f"{'Tax':<27}{self.money(totals['tax_amount']):>15}",
                f"{'Total Due':<27}{self.money(totals['due']):>15}",
                f"{'Paid':<27}{self.money(totals['cash_paid']):>15}",
                f"{'Change':<27}{self.money(totals['change']):>15}",
                "-" * 42,
                "Thank you for shopping with us.",
            ]
        )
        return "\n".join(lines)

    def save_receipt(self):
        if self.cart:
            receipt = self.build_receipt(self.current_totals(), completed=False)
        elif self.last_receipt_text:
            receipt = self.last_receipt_text
        else:
            messagebox.showinfo("No receipt", "There is no receipt to save yet.")
            return

        default_dir = Path.home() / "Desktop"
        if not default_dir.exists():
            default_dir = Path.home()

        filename = filedialog.asksaveasfilename(
            title="Save receipt",
            initialdir=str(default_dir),
            initialfile=f"receipt-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        )
        if not filename:
            return

        Path(filename).write_text(receipt, encoding="utf-8")
        self.set_status(f"Receipt saved to {filename}")

    def safe_float(self, value):
        try:
            return float(value or 0)
        except ValueError:
            return 0.0

    def money(self, amount):
        return f"{CURRENCY}{amount:,.2f}"

    def new_receipt_number(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    def set_status(self, message):
        self.status_var.set(message)


if __name__ == "__main__":
    root = tk.Tk()
    app = POS(root)
    root.mainloop()
