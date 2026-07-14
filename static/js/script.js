// ===============================
// Shorts Studio - script.js
// ===============================

// Show alert message
function showMessage(message) {
    alert(message);
}

// Confirm before deleting a video
function confirmDelete(videoName) {
    return confirm("Are you sure you want to delete:\n\n" + videoName + " ?");
}

// Search videos
function searchVideos() {
    let input = document.getElementById("searchInput");
    if (!input) return;

    let filter = input.value.toUpperCase();
    let cards = document.getElementsByClassName("video-card");

    for (let i = 0; i < cards.length; i++) {
        let title = cards[i].getElementsByTagName("h3")[0];

        if (title) {
            let txt = title.textContent || title.innerText;

            if (txt.toUpperCase().indexOf(filter) > -1) {
                cards[i].style.display = "";
            } else {
                cards[i].style.display = "none";
            }
        }
    }
}

// Preview selected video before upload
function previewVideo(input) {

    const preview = document.getElementById("videoPreview");

    if (!preview) return;

    if (input.files && input.files[0]) {

        preview.src = URL.createObjectURL(input.files[0]);

        preview.style.display = "block";

        preview.load();
    }
}

// Dark Mode Toggle
function toggleDarkMode() {

    document.body.classList.toggle("dark-mode");

    if(document.body.classList.contains("dark-mode")){
        localStorage.setItem("theme","dark");
    }else{
        localStorage.setItem("theme","light");
    }
}

// Load saved theme
window.onload = function(){

    if(localStorage.getItem("theme") === "dark"){
        document.body.classList.add("dark-mode");
    }

}
function filterCategory(category){

    const cards = document.querySelectorAll(".video-card");

    cards.forEach(card => {

        if(category === "All"){
            card.style.display = "block";
        }
        else{

            if(card.dataset.category === category){
                card.style.display = "block";
            }
            else{
                card.style.display = "none";
            }

        }

    });

}

