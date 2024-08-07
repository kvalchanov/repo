function reloadDivWithObjects(divId, objects) {
    const div = document.getElementById(divId);
    div.innerHTML = ''; // Clear existing content

    // Generate HTML content for each object
    objects.forEach(obj => {
        const itemHtml = `<div class="row>
            <div class="col-lg-4">
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
            </div>
        </div>`;
        div.innerHTML += itemHtml;
    });
}


document.addEventListener('DOMContentLoaded', () => {
    // The categories array will be passed from the main template
});
