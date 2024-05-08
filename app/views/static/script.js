function popisky_lenght(popisek) {
    if (popisek.length > 34) {
        return popisek.slice(0, 33) + "...";
    }
    return popisek;
}

function playlist_popisky_lenght(popisek) {
    if (popisek.length > 24) {
        return popisek.slice(0, 23) + "...";
    }
    return popisek;
}

document.querySelectorAll(".popisky").forEach(element => {
    element.textContent = popisky_lenght(element.textContent);
});

document.querySelectorAll(".playlist_popis").forEach(element => {
    element.textContent = playlist_popisky_lenght(element.textContent);
});

document.querySelectorAll(".popisky_play").forEach(element => {
    element.textContent = playlist_popisky_lenght(element.textContent);
});


function showPassword() {
    var passwordInput = document.getElementById("password");
    var visibleText = document.getElementById("visibleText");
    var passCheckbox = document.getElementById("passCheckbox");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        visibleText.textContent = "VISIBLE";
    } else {
        passwordInput.type = "password";
        visibleText.textContent = "";
    }
}

window.onload = function() {
var loginInputError = document.getElementById("loginInputError");
if (loginInputError) {
        setTimeout(function() {
        loginInputError.style.display = "none";
        }, 5000)
    }

};

window.onload = function() {
    var hotbar = document.getElementById("hotbar");
    var audio = document.getElementById("audioPlayer");
    var playButton = document.getElementById("playButton");
    var playButtonHotbar = document.getElementById("playButtonHotbar");
    var pauseButtonHotbar = document.getElementById("pauseButtonHotbar");

    playButton.addEventListener("click", function(event) {
        event.preventDefault();
        if (audio.paused) {
            audio.play();
        } else {
            audio.pause();
        }
    });

    playButtonHotbar.addEventListener("click", function(event) {
        event.preventDefault();
        audio.play();
    });

    pauseButtonHotbar.addEventListener("click", function(event) {
        event.preventDefault();
        audio.pause();
    });

    hotbar.style.display = "block";

    audio.src = "/static/Songy/Main Page Songz/Blinding Lights.mp3";
    audio.play();
};
