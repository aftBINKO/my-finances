const form = document.querySelector('.trans__form');
const typeInput = form.querySelector('[name="type"]');
const summaInput = form.querySelector('[name="sum"]');
const categoryInput = form.querySelector('[name="category"]');
const dateInput = form.querySelector('[name="date"]');

const listContainer = document.querySelector('.trans__list');
const template = document.querySelector('#trans__item-template');

function loadTrans() {
    const savedTrans = localStorage.getItem('my_transactions');
    if (savedTrans) {
        return JSON.parse(savedTrans);
    }
    return [];
}

function saveTrans(trans) {
    localStorage.setItem('my_transactions', JSON.stringify(trans));
}

let transss = loadTrans();

function addTrans(event) {
    event.preventDefault();

    const selectedDate = dateInput.value 

    const transssObj = {
        id: Date.now(), 
        type: typeInput.value,
        summa: Number(summaInput.value),
        category: categoryInput.value,
        data: selectedDate
    };

    transss.push(transssObj);
    saveTrans(transss);
    listTrans();
    updateDashboard();
    form.reset();
}

function listTrans() {
    if (!listContainer || !template) return;
    
    listContainer.innerHTML = '';

    const categoryTitles = {
        food: 'Еда',
        car: 'Транспорт',
        activity: 'Развлечения',
        study: 'Учеба',
        other: 'Другое'
    };

    transss.forEach((item) => {
        const clone = template.content.cloneNode(true);

        clone.querySelector('.date__item-text').textContent = item.data;
        clone.querySelector('.category__item-text').textContent = categoryTitles[item.category] || item.category;
        
        const sumTextNode = clone.querySelector('.sum__item-text');
        if (item.type === 'income') {
            sumTextNode.textContent = `+${item.summa} ₽`;
            sumTextNode.style.color = 'green';
        } else {
            sumTextNode.textContent = `-${item.summa} ₽`;
            sumTextNode.style.color = 'red';
        }

        const deleteBtn = clone.querySelector('.trans__item-button');
        deleteBtn.textContent = 'удалить';
        deleteBtn.addEventListener('click', () => deleteTrans(item.id));

        listContainer.appendChild(clone);
    });
}

function deleteTrans(id) {
    transss = transss.filter(item => item.id !== id); 
    saveTrans(transss);  
    listTrans();        
    updateDashboard();  
}

function updateDashboard() {
    const cards = document.querySelectorAll('.main-card p');
    if (cards.length < 3) return;
    
    let totalIncome = 0;
    let totalExpense = 0;

    transss.forEach(item => {
        if (item.type === 'income') {
            totalIncome += item.summa;
        } else {
            totalExpense += item.summa;
        }
    });

    const totalBalance = totalIncome - totalExpense;
    cards[0].textContent = `${totalBalance} ₽`;
    cards[1].textContent = `${totalIncome} ₽`;
    cards[2].textContent = `${totalExpense} ₽`;
}

form.addEventListener('submit', addTrans);

listTrans();
updateDashboard();
