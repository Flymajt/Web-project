function popisky_lenght(popisek) {
    if (popisek.length > 34) {
        return popisek.slice(0, 33) + "...";
    }
    return popisek;
}

function playlist_popisky_lenght(popisek) {
    if (popisek.length > 24) {
        if (popisek[22] === " ") {
            return popisek.slice(0, 21) + "...";
        } else {
            return popisek.slice(0, 23) + "...";
        }
    }
    return popisek;
}

function autor_popisky_lenght(popisek) {
    if (popisek.length > 24) {
        last_space = popisek.lastIndexOf(" ", 23);
        if (last_space !== -1) {
            updated_popisek = popisek.slice(0, last_space) + "<br>" + popisek.slice(last_space + 1);
            if (updated_popisek.length > 44) {
                if (updated_popisek[42] === " ") {
                    return updated_popisek.slice(0, 41) + "...";
                } else {
                    return updated_popisek.slice(0, 43) + "...";
                }
            }
            return updated_popisek;
        } else {
            if (popisek[22] === " ") {
                return popisek.slice(0, 21) + "...";
            } else {
                return popisek.slice(0, 23) + "...";
            }
        }
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
    element.innerHTML = autor_popisky_lenght(element.innerHTML);
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

// First onload (login error fade)
window.addEventListener("load", function () {
    var loginInputError = document.getElementById("loginInputError");
    if (loginInputError) {
        setTimeout(function () {
            loginInputError.style.display = "none";
        }, 5000);
    }

    // Live character count for About Me input
    const bioInput = document.getElementById("bioInput");
    const charCount = document.getElementById("charCount");

    if (bioInput && charCount) {
        charCount.textContent = `${bioInput.value.length} / 150 characters`;

        bioInput.addEventListener("input", () => {
            charCount.textContent = `${bioInput.value.length} / 150 characters`;
        });
    }
});

// Second onload (hotbar & audio player logic)
window.onload = function () {
    var playButtons = document.querySelectorAll(".playButton");
    var hotbar = document.getElementById("hotbar");
    var audio = new Audio();
    var lastVolume = 1;
    var lastSrc = "";
    var isRepeatOn = false;
    var muteButton = document.getElementById("muteButton");
    var repeatButton = document.getElementById("repeatButton");
    var playButtonHotbar = document.getElementById("playButtonHotbar");
    var pauseButtonHotbar = document.getElementById("pauseButtonHotbar");
    var rewindButton = document.getElementById("rewindButton");
    var forwardButton = document.getElementById("forwardButton");
    var volumeRange = document.getElementById("volumeRange");
    var hideHotbarButton = document.getElementById("hideHotbarButton");
    var previousButton = document.getElementById("previousButton");
    var nextButton = document.getElementById("nextButton");

    if (muteButton) {
        muteButton.addEventListener("click", function (event) {
            event.preventDefault();
            if (audio.volume !== 0) {
                lastVolume = audio.volume;
                audio.volume = 0;
                muteButton.textContent = "Zapnout zvuk";
            } else {
                audio.volume = lastVolume;
                muteButton.textContent = "Vypnout zvuk";
            }
        });
    }

    if (repeatButton) {
        repeatButton.addEventListener("click", function (event) {
            event.preventDefault();
            isRepeatOn = !isRepeatOn;
            repeatButton.textContent = isRepeatOn ? "Opakování zapnuto" : "Opakování vypnuto";
        });
    }

    playButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            var songSrc = button.getAttribute("data-src");
            audio.src = songSrc;
            audio.play();
            hotbar.style.display = "flex";
            lastSrc = songSrc;
        });
    });

    if (playButtonHotbar) {
        playButtonHotbar.addEventListener("click", function (event) {
            event.preventDefault();
            audio.play();
        });
    }

    if (pauseButtonHotbar) {
        pauseButtonHotbar.addEventListener("click", function (event) {
            event.preventDefault();
            audio.pause();
        });
    }

    if (rewindButton) {
        rewindButton.addEventListener("click", function (event) {
            event.preventDefault();
            audio.currentTime -= 15;
        });
    }

    if (forwardButton) {
        forwardButton.addEventListener("click", function (event) {
            event.preventDefault();
            audio.currentTime += 15;
        });
    }

    if (volumeRange) {
        volumeRange.addEventListener("input", function () {
            lastVolume = volumeRange.value;
            audio.volume = lastVolume;
        });
    }

    if (hideHotbarButton) {
        hideHotbarButton.addEventListener("click", function (event) {
            event.preventDefault();
            hotbar.style.transition = "opacity 0.5s, transform 0.5s";
            hotbar.style.opacity = "0";
            hotbar.style.transform = "translateY(100%)";
            setTimeout(function () {
                hotbar.style.display = "none";
            }, 500);
        });
    }

    if (previousButton) {
        previousButton.addEventListener("click", function (event) {
            event.preventDefault();
            var previousSongButton = document.querySelector('[data-src="' + lastSrc + '"]').parentNode.previousElementSibling.querySelector('.playButton');
            if (previousSongButton) {
                var previousSongSrc = previousSongButton.getAttribute("data-src");
                audio.src = previousSongSrc;
                audio.play();
                lastSrc = previousSongSrc;
            }
        });
    }

    if (nextButton) {
        nextButton.addEventListener("click", function (event) {
            event.preventDefault();
            var nextSongButton = document.querySelector('[data-src="' + lastSrc + '"]').parentNode.nextElementSibling.querySelector('.playButton');
            if (nextSongButton) {
                var nextSongSrc = nextSongButton.getAttribute("data-src");
                audio.src = nextSongSrc;
                audio.play();
                lastSrc = nextSongSrc;
            }
        });
    }

    audio.addEventListener("ended", function () {
        if (isRepeatOn) {
            audio.currentTime = 0;
            audio.play();
        } else {
            var nextSongButton = document.querySelector('[data-src="' + lastSrc + '"]').parentNode.nextElementSibling.querySelector('.playButton');
            if (nextSongButton) {
                var nextSongSrc = nextSongButton.getAttribute("data-src");
                audio.src = nextSongSrc;
                audio.play();
                lastSrc = nextSongSrc;
            }
        }
    });
};

document.getElementById("registerForm")?.addEventListener("submit", function (event) {
    const password = document.getElementById("registerPassword").value;
    const passwordError = document.getElementById("passwordError");
    const passwordPattern = /^(?=.*[A-Z])(?=.*\d).{6,}$/;

    if (!passwordPattern.test(password)) {
        passwordError.style.display = "block";
        event.preventDefault();
    } else {
        passwordError.style.display = "none";
    }
});


// bio


const bioInput = document.getElementById('bioInput');
const charCount = document.getElementById('charCount');

bioInput.addEventListener('input', () => {
    const currentLength = bioInput.value.length;
    charCount.textContent = `${currentLength} / 150 characters`;

    if (currentLength > 140) {
        charCount.style.color = 'red';
    } else if (currentLength > 100) {
        charCount.style.color = 'orange';
    } else {
        charCount.style.color = 'green';
    }
});

document.querySelector('form').addEventListener('submit', (event) => {
    if (bioInput.value.trim() === '') {
        event.preventDefault();
        alert('Your bio cannot be empty. Please write something about yourself!');
    }
});

bioInput.addEventListener('keypress', (event) => {
    const invalidChars = ['<', '>', '{', '}', '`', '$', '%', '^', '&', '*', '=', '+', '\\', '|', ';', ':', '"', "'", '[', ']', '~','/' ];
    if (invalidChars.includes(event.key)) {
        event.preventDefault();
        alert(`The character "${event.key}" is not allowed in the bio.`);
    }
});

bioInput.addEventListener('input', () => {
    const invalidCharsRegex = /[<>{}`$%^&*+=\\|;:"'\[\]~]/g;
    if (invalidCharsRegex.test(bioInput.value)) {
        bioInput.value = bioInput.value.replace(invalidCharsRegex, '');
        alert('Invalid characters have been removed from your bio.');
    }
});

