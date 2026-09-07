// ==========================================================================
// FALCON TRAVEL - MAIN APPLICATION JAVASCRIPT
// ==========================================================================

document.addEventListener('DOMContentLoaded', function() {
    // ----------------------------------------------------------------------
    // 1. Hero Video Cycling (Sheet 1)
    // ----------------------------------------------------------------------
    var video1 = document.getElementById('video1');
    var video2 = document.getElementById('video2');
    var video3 = document.getElementById('video3');

    if (video1 && video2 && video3) {
        video1.onended = function() {
            video2.play().catch(function(e){});
            video1.style.opacity = 0;
            video2.style.opacity = 1;
        };

        video2.onended = function() {
            video3.play().catch(function(e){});
            video2.style.opacity = 0;
            video3.style.opacity = 1;
        };

        video3.onended = function() {
            video1.play().catch(function(e){});
            video3.style.opacity = 0;
            video1.style.opacity = 1;
        };
    }

    // ----------------------------------------------------------------------
    // 2. Featured Packages Slider (Sheet 3 - TinySlider)
    // ----------------------------------------------------------------------
    var sliderContainer = document.querySelector(".my-slider");
    if (sliderContainer && typeof tns === 'function') {
        try {
            var slider = tns({
                container: ".my-slider",
                slideBy: 1,
                speed: 500,
                nav: false,
                autoplay: true,
                autoplayHoverPause: true,
                controls: false,
                autoplayButtonOutput: false,
                mouseDrag: true,
                touch: true,
                items: 1,
                gutter: 15,
                responsive: {
                    0: {
                        items: 1,
                        gutter: 10
                    },
                    576: {
                        items: 2,
                        gutter: 15
                    },
                    992: {
                        items: 3,
                        gutter: 20
                    },
                    1200: {
                        items: 4,
                        gutter: 20
                    }
                }
            });
        } catch (err) {
            console.warn("TinySlider init:", err);
        }
    }

    // ----------------------------------------------------------------------
    // 3. Popular Destinations Swiper (Sheet 4 - Swiper)
    // ----------------------------------------------------------------------
    var swiperContainer = document.querySelector('.s4__swiper');
    if (swiperContainer && typeof Swiper === 'function') {
        try {
            var swiperHome = new Swiper('.s4__swiper', {
                loop: true,
                spaceBetween: 20,
                grabCursor: true,
                slidesPerView: 'auto',
                centeredSlides: false,
                autoplay: {
                    delay: 3500,
                    disableOnInteraction: false,
                },
                breakpoints: {
                    320: {
                        spaceBetween: 15,
                    },
                    768: {
                        spaceBetween: 20,
                    },
                    1200: {
                        spaceBetween: 25,
                    }
                }
            });
        } catch (err) {
            console.warn("Swiper init:", err);
        }
    }

    // ----------------------------------------------------------------------
    // 4. Input Focus Effects
    // ----------------------------------------------------------------------
    var inputs = document.querySelectorAll(".input");
    inputs.forEach(function(input) {
        input.addEventListener("focus", function() {
            if (this.parentNode) {
                this.parentNode.classList.add("focus");
            }
        });
        input.addEventListener("blur", function() {
            if (this.parentNode && this.value === "") {
                this.parentNode.classList.remove("focus");
            }
        });
    });
});