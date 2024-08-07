// static/pagination.js
let categories = [];
let page = 1;
const pageSize = 6;
let totalPages = 0;

function initializePagination(initialCategories) {
    categories = initialCategories;
    totalPages = Math.ceil(categories.length / pageSize);
    renderPage();
}

function renderPage() {
    const start = (page - 1) * pageSize;
    const end = start + pageSize;
    const paginatedCategories = categories.slice(start, end);

    let categoriesHtml = "";
    for (const category of paginatedCategories) {
        categoriesHtml += `<div class="col-lg-4">
            <a href="${category.id}">
                <div class="item">
                    <div class="thumb">
                        <img src="../../static/images/men-01.jpg" alt="">
                    </div>
                    <div class="down-content">
                        <h4>${category.name}</h4>
                    </div>
                </div>
            </a>
        </div>`
    }

    // Append categories to the existing container
    document.querySelector('.row').innerHTML = categoriesHtml;

    document.getElementById('current-page').innerText = `Page ${page}`;
    updateButtons();
}

function updateButtons() {
    document.getElementById('prev-button').disabled = page === 1;
    document.getElementById('next-button').disabled = page === totalPages;
}

function loadPage(newPage) {
    if (newPage < 1 || newPage > totalPages) return;
    page = newPage;
    renderPage();
}

document.addEventListener('DOMContentLoaded', () => {
    // The categories array will be passed from the main template
});
