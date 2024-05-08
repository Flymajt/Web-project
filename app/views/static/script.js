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
    var playButtonHotbar = document.getElementById("playButtonHotbar");
    var pauseButtonHotbar = document.getElementById("pauseButtonHotbar");
    var rewindButton = document.getElementById("rewindButton");
    var forwardButton = document.getElementById("forwardButton");
    var volumeRange = document.getElementById("volumeRange");
    var currentSongIndex = 0;

    playButtonHotbar.addEventListener("click", function(event) {
        event.preventDefault();
        audio.play();
    });

    pauseButtonHotbar.addEventListener("click", function(event) {
        event.preventDefault();
        audio.pause();
    });

    rewindButton.addEventListener("click", function(event) {
        event.preventDefault();
        audio.currentTime -= 15;
    });

    forwardButton.addEventListener("click", function(event) {
        event.preventDefault();
        audio.currentTime += 15;
    });

    volumeRange.addEventListener("input", function() {
        audio.volume = volumeRange.value;
    });

    hotbar.style.display = "block";

    var images = document.querySelectorAll(".playButton");
    images.forEach(function(image, index) {
        image.addEventListener("click", function(event) {
            event.preventDefault();
            var songSrc = image.getAttribute("data-src");
            audio.src = songSrc;
            currentSongIndex = index;
            audio.play();
        });
    });

    audio.addEventListener("ended", function() {
    });

    audio.src = "";
};