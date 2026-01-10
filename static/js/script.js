/* ========================================
   SAFO POS - MAIN APPLICATION
   ======================================== */

const App = {
    /* ========================================
       DATA STORAGE
       ======================================== */
    products: [
        { id: 1, name: "Coca Cola 1L", barcode: "4870123456789", price: 8000, quantity: 50 },
        { id: 2, name: "Lay's chips", barcode: "4870123456790", price: 5000, quantity: 100 },
        { id: 3, name: "Nestle qahva", barcode: "4870123456791", price: 25000, quantity: 30 },
        { id: 4, name: "Snickers", barcode: "4870123456792", price: 3500, quantity: 150 },
        { id: 5, name: "Red Bull", barcode: "4870123456793", price: 12000, quantity: 40 },
        { id: 6, name: "Bounty", barcode: "4870123456794", price: 3500, quantity: 120 },
        { id: 7, name: "Kitkat", barcode: "4870123456795", price: 4000, quantity: 90 },
        { id: 8, name: "Pepsi 1.5L", barcode: "4870123456796", price: 9000, quantity: 60 },
        { id: 9, name: "Fanta 1L", barcode: "4870123456797", price: 7500, quantity: 70 },
        { id: 10, name: "Sprite 1L", barcode: "4870123456798", price: 7500, quantity: 65 }
    ],
    
    customers: [
        { id: 1, firstName: "Alisher", lastName: "Karimov", phone: "+998901234567", debt: 50000 },
        { id: 2, firstName: "Dilnoza", lastName: "Rakhimova", phone: "+998901234568", debt: 0 },
        { id: 3, firstName: "Bekzod", lastName: "Tursunov", phone: "+998901234569", debt: 120000 },
        { id: 4, firstName: "Sevara", lastName: "Abdullayeva", phone: "+998901234570", debt: 25000 },
        { id: 5, firstName: "Jasur", lastName: "Sharipov", phone: "+998901234571", debt: 0 }
    ],
    
    currentSale: [],
    sales: [],
    currentEditSaleId: null,
    currentEditCustomerId: null,
    confirmCallback: null,
    selectedCustomer: null,
    
    
    /* ========================================
       INITIALIZATION
       ======================================== */
    init() {
        this.loadFromStorage();
        this.setupEventListeners();
        this.renderProducts();
        this.renderCustomers();
        this.renderSales();
    },
    
    loadFromStorage() {
        const storedSales = localStorage.getItem('safo_pos_sales');
        if (storedSales) {
            this.sales = JSON.parse(storedSales);
        }
        
        const storedCustomers = localStorage.getItem('safo_pos_customers');
        if (storedCustomers) {
            this.customers = JSON.parse(storedCustomers);
        }
    },
    
    saveToStorage() {
        localStorage.setItem('safo_pos_sales', JSON.stringify(this.sales));
        localStorage.setItem('safo_pos_customers', JSON.stringify(this.customers));
    },
    
    
    /* ========================================
       EVENT LISTENERS SETUP
       ======================================== */
    setupEventListeners() {
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebarToggle');
        
        // Sidebar toggle
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
        });
        
        // Mobile sidebar
        if (window.innerWidth <= 768) {
            sidebar.classList.add('active');
        }
        
        // Navigation items
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const section = item.getAttribute('data-section');
                this.switchSection(section);
                
                navItems.forEach(nav => nav.classList.remove('active'));
                item.classList.add('active');
                
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('active');
                }
            });
        });
        
        // Product search
        document.getElementById('productSearch').addEventListener('input', (e) => {
            this.searchProduct(e.target.value);
        });
        
        // Action buttons
        document.getElementById('productsBtn').addEventListener('click', () => {
            this.openProductModal();
        });
        
        document.getElementById('selectCustomerBtn').addEventListener('click', () => {
            this.openSelectCustomerModal();
        });
        
        document.getElementById('clearSaleBtn').addEventListener('click', () => {
            this.clearSale();
        });
        
        // Modal close buttons
        document.getElementById('closeProductModal').addEventListener('click', () => {
            this.closeProductModal();
        });
        
        document.getElementById('closeSelectCustomerModal').addEventListener('click', () => {
            this.closeSelectCustomerModal();
        });
        
        document.getElementById('removeCustomerBtn').addEventListener('click', () => {
            this.removeSelectedCustomer();
        });
        
        // Payment
        document.getElementById('paidAmount').addEventListener('input', () => {
            this.updateDiscount();
        });
        
        document.getElementById('completeSaleBtn').addEventListener('click', () => {
            this.completeSale();
        });
        
        // Modal searches
        document.getElementById('modalProductSearch').addEventListener('input', (e) => {
            this.filterModalProducts(e.target.value);
        });
        
        document.getElementById('modalCustomerSearch').addEventListener('input', (e) => {
            this.filterModalCustomers(e.target.value);
        });
        
        document.getElementById('productFilterSearch').addEventListener('input', (e) => {
            this.filterProductsTable(e.target.value);
        });
        
        // Sale editing
        document.getElementById('closeEditSaleModal').addEventListener('click', () => {
            this.closeEditSaleModal();
        });
        
        document.getElementById('saveEditSaleBtn').addEventListener('click', () => {
            this.saveEditedSale();
        });
        
        document.getElementById('deleteSaleBtn').addEventListener('click', () => {
            this.deleteSale();
        });
        
        document.getElementById('editPaidAmount').addEventListener('input', () => {
            this.updateEditDiscount();
        });
        
        // Customer management
        document.getElementById('addCustomerBtn').addEventListener('click', () => {
            this.openCustomerModal();
        });
        
        document.getElementById('closeCustomerModal').addEventListener('click', () => {
            this.closeCustomerModal();
        });
        
        document.getElementById('cancelCustomerBtn').addEventListener('click', () => {
            this.closeCustomerModal();
        });
        
        document.getElementById('saveCustomerBtn').addEventListener('click', () => {
            this.saveCustomer();
        });
        
        // Confirmation modals
        document.getElementById('confirmOkBtn').addEventListener('click', () => {
            if (this.confirmCallback) {
                this.confirmCallback();
                this.confirmCallback = null;
            }
            this.closeConfirmModal();
        });
        
        document.getElementById('confirmCancelBtn').addEventListener('click', () => {
            this.closeConfirmModal();
        });
        
        document.getElementById('alertOkBtn').addEventListener('click', () => {
            this.closeAlertModal();
        });
    },
    
    
    /* ========================================
       NAVIGATION & SECTIONS
       ======================================== */
    switchSection(sectionName) {
        const sections = document.querySelectorAll('.section');
        sections.forEach(section => section.classList.remove('active'));
        
        const targetSection = document.getElementById(`section-${sectionName}`);
        if (targetSection) {
            targetSection.classList.add('active');
        }
        
        const breadcrumb = document.getElementById('breadcrumb');
        const sectionNames = {
            'yangi-savdo': 'Savdo > Yangi savdo',
            'savdolar': 'Savdolar',
            'mahsulotlar': 'Mahsulotlar',
            'mijozlar': 'Mijozlar',
            'hisobotlar': 'Hisobotlar',
            'sozlamalar': 'Sozlamalar'
        };
        breadcrumb.textContent = sectionNames[sectionName] || sectionName;
    },
    
    
    /* ========================================
       PRODUCT MANAGEMENT
       ======================================== */
    searchProduct(query) {
        if (!query) return;
        
        query = query.toLowerCase();
        const product = this.products.find(p => 
            p.barcode.includes(query) || 
            p.name.toLowerCase().includes(query)
        );
        
        if (product) {
            this.addToSale(product);
            document.getElementById('productSearch').value = '';
        }
    },
    
    addToSale(product) {
        const existing = this.currentSale.find(item => item.id === product.id);
        
        if (existing) {
            existing.quantity++;
        } else {
            this.currentSale.push({
                id: product.id,
                name: product.name,
                barcode: product.barcode,
                price: product.price,
                quantity: 1
            });
        }
        
        this.renderSaleTable();
        this.updateTotals();
    },
    
    renderSaleTable() {
        const tbody = document.getElementById('saleTableBody');
        
        if (this.currentSale.length === 0) {
            tbody.innerHTML = '<tr class="empty-state"><td colspan="6">Savdo bo\'sh. Mahsulot qo\'shing.</td></tr>';
            return;
        }
        
        tbody.innerHTML = this.currentSale.map((item, index) => `
            <tr>
                <td>${item.name}</td>
                <td>${item.barcode}</td>
                <td>${this.formatPrice(item.price)}</td>
                <td>
                    <div class="qty-controls">
                        <button class="qty-btn" onclick="App.decreaseQuantity(${index})">−</button>
                        <input type="number" class="qty-input" value="${item.quantity}" 
                               onchange="App.updateQuantity(${index}, this.value)" min="1">
                        <button class="qty-btn" onclick="App.increaseQuantity(${index})">+</button>
                    </div>
                </td>
                <td>${this.formatPrice(item.price * item.quantity)}</td>
                <td>
                    <button class="remove-btn" onclick="App.removeFromSale(${index})">🗑️</button>
                </td>
            </tr>
        `).join('');
    },
    
    increaseQuantity(index) {
        this.currentSale[index].quantity++;
        this.renderSaleTable();
        this.updateTotals();
    },
    
    decreaseQuantity(index) {
        if (this.currentSale[index].quantity > 1) {
            this.currentSale[index].quantity--;
            this.renderSaleTable();
            this.updateTotals();
        }
    },
    
    updateQuantity(index, value) {
        const qty = parseInt(value);
        if (qty > 0) {
            this.currentSale[index].quantity = qty;
            this.renderSaleTable();
            this.updateTotals();
        }
    },
    
    removeFromSale(index) {
        this.currentSale.splice(index, 1);
        this.renderSaleTable();
        this.updateTotals();
    },
    
    
    /* ========================================
       PAYMENT & TOTALS
       ======================================== */
    updateTotals() {
        const total = this.currentSale.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        document.getElementById('totalAmount').textContent = this.formatPrice(total);
        this.updateDiscount();
    },
    
    updateDiscount() {
        const total = this.currentSale.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        const paid = parseInt(document.getElementById('paidAmount').value) || 0;
        const discountAmount = document.getElementById('discountAmount');
        
        const discount = total - paid;
        if (discount > 0) {
            discountAmount.textContent = this.formatPrice(discount);
        } else {
            discountAmount.textContent = '0 so\'m';
        }
    },
    
    clearSale() {
        if (this.currentSale.length === 0) return;
        
        this.showConfirm('Savdoni tozalashni xohlaysizmi?', '🗑️', () => {
            this.currentSale = [];
            this.selectedCustomer = null;
            this.updateSelectedCustomerDisplay();
            this.renderSaleTable();
            this.updateTotals();
            document.getElementById('paidAmount').value = '';
        });
    },
    
    completeSale() {
        if (this.currentSale.length === 0) {
            this.showAlert('Savdo bo\'sh. Mahsulot qo\'shing.', '⚠️');
            return;
        }
        
        const total = this.currentSale.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        const paid = parseInt(document.getElementById('paidAmount').value) || 0;
        const paymentType = document.querySelector('input[name="paymentType"]:checked').value;
        const discount = total - paid;
        
        const sale = {
            id: Date.now(),
            items: [...this.currentSale],
            customer: this.selectedCustomer ? {...this.selectedCustomer} : null,
            total: total,
            paid: paid,
            discount: discount > 0 ? discount : 0,
            paymentType: paymentType,
            date: new Date()
        };
        
        this.sales.unshift(sale);
        this.saveToStorage();
        this.renderSales();
        
        this.currentSale = [];
        this.selectedCustomer = null;
        this.updateSelectedCustomerDisplay();
        this.renderSaleTable();
        this.updateTotals();
        document.getElementById('paidAmount').value = '';
        
        this.showAlert('Savdo muvaffaqiyatli yakunlandi!', '✅');
    },
    
    
    /* ========================================
       PRODUCT MODAL
       ======================================== */
    openProductModal() {
        const modal = document.getElementById('productModal');
        modal.classList.add('active');
        this.renderModalProducts();
    },
    
    closeProductModal() {
        const modal = document.getElementById('productModal');
        modal.classList.remove('active');
    },
    
    renderModalProducts(filteredProducts = null) {
        const container = document.getElementById('modalProductsList');
        const productsToShow = filteredProducts || this.products;
        
        container.innerHTML = productsToShow.map(product => `
            <div class="product-card" onclick="App.selectProductFromModal(${product.id})">
                <div class="product-card-title">${product.name}</div>
                <div class="product-card-info">Barcode: ${product.barcode}</div>
                <div class="product-card-info">Omborda: ${product.quantity} ta</div>
                <div class="product-card-price">${this.formatPrice(product.price)}</div>
                <button class="product-card-btn" onclick="event.stopPropagation(); App.selectProductFromModal(${product.id})">
                    Tanlash
                </button>
            </div>
        `).join('');
    },
    
    filterModalProducts(query) {
        if (!query) {
            this.renderModalProducts();
            return;
        }
        
        query = query.toLowerCase();
        const filtered = this.products.filter(p => 
            p.name.toLowerCase().includes(query) ||
            p.barcode.includes(query)
        );
        this.renderModalProducts(filtered);
    },
    
    selectProductFromModal(productId) {
        const product = this.products.find(p => p.id === productId);
        if (product) {
            this.addToSale(product);
            this.closeProductModal();
        }
    },
    
    
    /* ========================================
       CUSTOMER SELECTION
       ======================================== */
    openSelectCustomerModal() {
        const modal = document.getElementById('selectCustomerModal');
        modal.classList.add('active');
        this.renderModalCustomers();
    },
    
    closeSelectCustomerModal() {
        const modal = document.getElementById('selectCustomerModal');
        modal.classList.remove('active');
    },
    
    renderModalCustomers(filteredCustomers = null) {
        const container = document.getElementById('modalCustomersList');
        const customersToShow = filteredCustomers || this.customers;
        
        container.innerHTML = customersToShow.map(customer => `
            <div class="customer-card" onclick="App.selectCustomerFromModal(${customer.id})">
                <div class="customer-card-icon">👤</div>
                <div class="customer-card-name">${customer.firstName} ${customer.lastName}</div>
                <div class="customer-card-info">${customer.phone}</div>
                <div class="customer-card-debt ${customer.debt === 0 ? 'no-debt' : ''}">
                    ${customer.debt > 0 ? 'Qarz: ' + this.formatPrice(customer.debt) : 'Qarzi yo\'q'}
                </div>
                <button class="customer-card-btn" onclick="event.stopPropagation(); App.selectCustomerFromModal(${customer.id})">
                    Tanlash
                </button>
            </div>
        `).join('');
    },
    
    filterModalCustomers(query) {
        if (!query) {
            this.renderModalCustomers();
            return;
        }
        
        query = query.toLowerCase();
        const filtered = this.customers.filter(c => 
            c.firstName.toLowerCase().includes(query) ||
            c.lastName.toLowerCase().includes(query) ||
            c.phone.includes(query)
        );
        this.renderModalCustomers(filtered);
    },
    
    selectCustomerFromModal(customerId) {
        const customer = this.customers.find(c => c.id === customerId);
        if (customer) {
            this.selectedCustomer = customer;
            this.updateSelectedCustomerDisplay();
            this.closeSelectCustomerModal();
        }
    },
    
    updateSelectedCustomerDisplay() {
        const container = document.getElementById('selectedCustomerInfo');
        const nameEl = document.getElementById('selectedCustomerName');
        const phoneEl = document.getElementById('selectedCustomerPhone');
        
        if (this.selectedCustomer) {
            nameEl.textContent = `${this.selectedCustomer.firstName} ${this.selectedCustomer.lastName}`;
            phoneEl.textContent = this.selectedCustomer.phone;
            container.style.display = 'block';
        } else {
            container.style.display = 'none';
        }
    },
    
    removeSelectedCustomer() {
        this.selectedCustomer = null;
        this.updateSelectedCustomerDisplay();
    },
    
    
    /* ========================================
       PRODUCTS TABLE
       ======================================== */
    renderProducts() {
        const tbody = document.getElementById('productsTableBody');
        tbody.innerHTML = this.products.map(product => `
            <tr>
                <td>${product.name}</td>
                <td>${product.barcode}</td>
                <td>${this.formatPrice(product.price)}</td>
                <td>${product.quantity}</td>
            </tr>
        `).join('');
    },
    
    filterProductsTable(query) {
        const tbody = document.getElementById('productsTableBody');
        
        if (!query) {
            this.renderProducts();
            return;
        }
        
        query = query.toLowerCase();
        const filtered = this.products.filter(p => 
            p.name.toLowerCase().includes(query) ||
            p.barcode.includes(query)
        );
        
        tbody.innerHTML = filtered.map(product => `
            <tr>
                <td>${product.name}</td>
                <td>${product.barcode}</td>
                <td>${this.formatPrice(product.price)}</td>
                <td>${product.quantity}</td>
            </tr>
        `).join('');
    },
    
    
    /* ========================================
       CUSTOMER MANAGEMENT
       ======================================== */
    renderCustomers() {
        const tbody = document.getElementById('customersTableBody');
        tbody.innerHTML = this.customers.map(customer => `
            <tr>
                <td>${customer.firstName}</td>
                <td>${customer.lastName}</td>
                <td>${customer.phone}</td>
                <td>${this.formatPrice(customer.debt)}</td>
                <td>
                    <button class="action-btn edit" onclick="App.editCustomer(${customer.id})" title="Tahrirlash">✏️</button>
                    <button class="action-btn delete" onclick="App.deleteCustomer(${customer.id})" title="O'chirish">🗑️</button>
                </td>
            </tr>
        `).join('');
    },
    
    openCustomerModal(customer = null) {
        const modal = document.getElementById('customerModal');
        const modalTitle = document.getElementById('customerModalTitle');
        
        if (customer) {
            modalTitle.textContent = 'Mijozni tahrirlash';
            document.getElementById('customerFirstName').value = customer.firstName;
            document.getElementById('customerLastName').value = customer.lastName;
            document.getElementById('customerPhone').value = customer.phone;
            document.getElementById('customerDebt').value = customer.debt;
            this.currentEditCustomerId = customer.id;
        } else {
            modalTitle.textContent = 'Yangi mijoz qo\'shish';
            document.getElementById('customerFirstName').value = '';
            document.getElementById('customerLastName').value = '';
            document.getElementById('customerPhone').value = '';
            document.getElementById('customerDebt').value = '0';
            this.currentEditCustomerId = null;
        }
        
        modal.classList.add('active');
    },
    
    closeCustomerModal() {
        const modal = document.getElementById('customerModal');
        modal.classList.remove('active');
        this.currentEditCustomerId = null;
    },
    
    saveCustomer() {
        const firstName = document.getElementById('customerFirstName').value.trim();
        const lastName = document.getElementById('customerLastName').value.trim();
        const phone = document.getElementById('customerPhone').value.trim();
        const debt = parseInt(document.getElementById('customerDebt').value) || 0;
        
        if (!firstName || !lastName || !phone) {
            this.showAlert('Iltimos, barcha maydonlarni to\'ldiring!', '⚠️');
            return;
        }
        
        if (this.currentEditCustomerId) {
            const customer = this.customers.find(c => c.id === this.currentEditCustomerId);
            if (customer) {
                customer.firstName = firstName;
                customer.lastName = lastName;
                customer.phone = phone;
                customer.debt = debt;
            }
        } else {
            const newCustomer = {
                id: Date.now(),
                firstName: firstName,
                lastName: lastName,
                phone: phone,
                debt: debt
            };
            this.customers.push(newCustomer);
        }
        
        this.saveToStorage();
        this.renderCustomers();
        this.closeCustomerModal();
        this.showAlert(
            this.currentEditCustomerId ? 'Mijoz yangilandi!' : 'Yangi mijoz qo\'shildi!',
            '✅'
        );
    },
    
    editCustomer(customerId) {
        const customer = this.customers.find(c => c.id === customerId);
        if (customer) {
            this.openCustomerModal(customer);
        }
    },
    
    deleteCustomer(customerId) {
        this.showConfirm('Mijozni o\'chirmoqchimisiz?', '🗑️', () => {
            this.customers = this.customers.filter(c => c.id !== customerId);
            this.saveToStorage();
            this.renderCustomers();
            this.showAlert('Mijoz o\'chirildi!', '✅');
        });
    },
    
    
    /* ========================================
       SALES MANAGEMENT
       ======================================== */
    renderSales() {
        const tbody = document.getElementById('salesTableBody');
        
        if (this.sales.length === 0) {
            tbody.innerHTML = '<tr class="empty-state"><td colspan="6">Hozircha savdolar yo\'q</td></tr>';
            return;
        }
        
        tbody.innerHTML = this.sales.map(sale => {
            const date = new Date(sale.date);
            return `
                <tr onclick="App.openEditSaleModal(${sale.id})">
                    <td>#${sale.id}</td>
                    <td>${this.formatPrice(sale.total)}</td>
                    <td>${this.formatPrice(sale.paid)}</td>
                    <td>${this.formatPrice(sale.discount)}</td>
                    <td>${this.formatTime(date)}</td>
                    <td>${this.formatDate(date)}</td>
                </tr>
            `;
        }).join('');
    },
    
    openEditSaleModal(saleId) {
        const sale = this.sales.find(s => s.id === saleId);
        if (!sale) return;
        
        this.currentEditSaleId = saleId;
        
        const tbody = document.getElementById('editSaleTableBody');
        tbody.innerHTML = sale.items.map((item, index) => `
            <tr>
                <td>${item.name}</td>
                <td>
                    <input type="number" class="qty-input" value="${item.price}" 
                           onchange="App.updateEditPrice(${index}, this.value)" min="0">
                </td>
                <td>
                    <div class="qty-controls">
                        <button class="qty-btn" onclick="App.decreaseEditQuantity(${index})">−</button>
                        <input type="number" class="qty-input" value="${item.quantity}" 
                               onchange="App.updateEditQuantity(${index}, this.value)" min="1">
                        <button class="qty-btn" onclick="App.increaseEditQuantity(${index})">+</button>
                    </div>
                </td>
                <td>${this.formatPrice(item.price * item.quantity)}</td>
            </tr>
        `).join('');
        
        document.getElementById('editPaidAmount').value = sale.paid;
        this.updateEditTotals();
        
        const modal = document.getElementById('editSaleModal');
        modal.classList.add('active');
    },
    
    closeEditSaleModal() {
        const modal = document.getElementById('editSaleModal');
        modal.classList.remove('active');
        this.currentEditSaleId = null;
    },
    
    increaseEditQuantity(index) {
        const sale = this.sales.find(s => s.id === this.currentEditSaleId);
        if (sale) {
            sale.items[index].quantity++;
            this.openEditSaleModal(this.currentEditSaleId);
        }
    },
    
    decreaseEditQuantity(index) {
        const sale = this.sales.find(s => s.id === this.currentEditSaleId);
        if (sale && sale.items[index].quantity > 1) {
            sale.items[index].quantity--;
            this.openEditSaleModal(this.currentEditSaleId);
        }
    },
    
    updateEditQuantity(index, value) {
        const qty = parseInt(value);
        const sale = this.sales.find(s => s.id === this.currentEditSaleId);
        if (sale && qty > 0) {
            sale.items[index].quantity = qty;
            this.openEditSaleModal(this.currentEditSaleId);
        }
    },
    
    updateEditPrice(index, value) {
        const price = parseInt(value);
        const sale = this.sales.find(s => s.id === this.currentEditSaleId);
        if (sale && price >= 0) {
            sale.items[index].price = price;
            this.openEditSaleModal(this.currentEditSaleId);
        }
    },
    
    updateEditTotals() {
        const sale = this.sales.find(s => s.id === this.currentEditSaleId);
        if (sale) {
            const total = sale.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            document.getElementById('editTotalAmount').textContent = this.formatPrice(total);
            this.updateEditDiscount();
        }
    },
    
    updateEditDiscount() {
        const sale = this.sales.find(s => s.id === this.currentEditSaleId);
        if (sale) {
            const total = sale.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            const paid = parseInt(document.getElementById('editPaidAmount').value) || 0;
            const discount = total - paid;
            
            if (discount > 0) {
                document.getElementById('editDiscountAmount').textContent = this.formatPrice(discount);
            } else {
                document.getElementById('editDiscountAmount').textContent = '0 so\'m';
            }
        }
    },
    
    saveEditedSale() {
        const sale = this.sales.find(s => s.id === this.currentEditSaleId);
        if (sale) {
            sale.total = sale.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            sale.paid = parseInt(document.getElementById('editPaidAmount').value) || 0;
            sale.discount = sale.total - sale.paid;
            if (sale.discount < 0) sale.discount = 0;
            
            this.saveToStorage();
            this.renderSales();
            this.closeEditSaleModal();
            this.showAlert('Savdo saqlandi!', '✅');
        }
    },
    
    deleteSale() {
        this.showConfirm('Savdoni o\'chirmoqchimisiz?', '🗑️', () => {
            this.sales = this.sales.filter(s => s.id !== this.currentEditSaleId);
            this.saveToStorage();
            this.renderSales();
            this.closeEditSaleModal();
            this.showAlert('Savdo o\'chirildi!', '✅');
        });
    },
    
    
    /* ========================================
       MODAL DIALOGS
       ======================================== */
    showConfirm(message, icon, callback) {
        const modal = document.getElementById('confirmModal');
        document.getElementById('confirmMessage').textContent = message;
        document.getElementById('confirmIcon').textContent = icon;
        this.confirmCallback = callback;
        modal.classList.add('active');
    },
    
    closeConfirmModal() {
        const modal = document.getElementById('confirmModal');
        modal.classList.remove('active');
        this.confirmCallback = null;
    },
    
    showAlert(message, icon) {
        const modal = document.getElementById('alertModal');
        document.getElementById('alertMessage').textContent = message;
        document.getElementById('alertIcon').textContent = icon;
        modal.classList.add('active');
    },
    
    closeAlertModal() {
        const modal = document.getElementById('alertModal');
        modal.classList.remove('active');
    },
    
    
    /* ========================================
       UTILITY FUNCTIONS
       ======================================== */
    formatPrice(price) {
        return new Intl.NumberFormat('uz-UZ').format(price) + ' so\'m';
    },
    
    formatTime(date) {
        return date.toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' });
    },
    
    formatDate(date) {
        const months = [
            'yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun',
            'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr'
        ];
        
        const day = date.getDate();
        const month = months[date.getMonth()];
        const year = date.getFullYear();
        
        return `${day}-${month} ${year}`;
    }
};


/* ========================================
   APPLICATION STARTUP
   ======================================== */
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});