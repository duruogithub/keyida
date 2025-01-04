// scripts.js

document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript is loaded!");

    // Example: Display a message when a button is clicked
    const button = document.querySelector("button");
    if (button) {
        button.addEventListener("click", () => {
            alert("Button clicked!");
        });
    }
});