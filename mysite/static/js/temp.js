const slidePage = document.querySelector(".slidepage");
const nextBtnFir = document.querySelector(".nextBtn");
const prevBtnSec = document.querySelector(".prev-1");
const nextBtnSec = document.querySelector(".next-1");
const prevBtnThir = document.querySelector(".prev-2");
const submitBtn = document.querySelector(".submit");

/* 페이지 넘기기*/
nextBtnFir.addEventListener("click", function(){
    slidePage.style.marginLeft = "-25%";
});
nextBtnSec.addEventListener("click", function(){
    slidePage.style.marginLeft = "-50%";
});


/* 페이지 뒤로 가기 */ 
prevBtnSec.addEventListener("click", function(){
    slidePage.style.marginLeft = "0%";
});
prevBtnThir.addEventListener("click", function(){
    slidePage.style.marginLeft = "-25%";
});


/* 첫번째 버튼 클릭 시 배경 변경 및 값 저장*/ 
var caf = 3;
function change_firbtn(e) {
    var btns = document.querySelectorAll(".field");
    btns.forEach(function (btn, i) {
      if (e.currentTarget == btn) {
        btn.classList.add("active");
        caf = e.target.value
        console.log(caf);
      } else {
        btn.classList.remove("active");
      }
    });
}

/* 첫번째 버튼 클릭 시 배경 변경 및 값 저장*/ 
var caf = 3;
function change_secbtn(e) {
    var btns = document.querySelectorAll(".field");
    btns.forEach(function (btn, i) {
      if (e.currentTarget == btn) {
        btn.classList.add("active");
        caf = e.target.value
        console.log(caf);
      } else {
        btn.classList.remove("active");
      }
    });
}


