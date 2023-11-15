

var swiper = new Swiper(".slide-content", {
    slidesPerView: 3,
    spaceBetween: 20,
    slidesPerGroup: 3,
    loop: true,
    loopFillGroupWithBlank: true,
    gragCursor:"true",
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });