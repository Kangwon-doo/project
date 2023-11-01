const slidePage = document.querySelector(".slidepage");
const nextBtnFir = document.querySelector(".nextBtn");
const prevBtnSec = document.querySelector(".prev-1");
const nextBtnSec = document.querySelector(".next-1");
const prevBtnThir = document.querySelector(".prev-2");
const nextBtnThir = document.querySelector(".next-2");
const prevBtnFour = document.querySelector(".prev-3");
const submitBtn = document.querySelector(".submit");


/* 페이지 넘기기*/
nextBtnFir.addEventListener("click", function(){
    slidePage.style.marginLeft = "-25%";
});
nextBtnSec.addEventListener("click", function(){
    slidePage.style.marginLeft = "-50%";
});
nextBtnThir.addEventListener("click", function(){
    slidePage.style.marginLeft = "-75%";
});

/* 페이지 뒤로 가기 */ 
prevBtnSec.addEventListener("click", function(){
    slidePage.style.marginLeft = "0%";
});
prevBtnThir.addEventListener("click", function(){
    slidePage.style.marginLeft = "-25%";
});
prevBtnFour.addEventListener("click", function(){
    slidePage.style.marginLeft = "-50%";
});


/* 1번째 질문 페이지 버튼 클릭 시 배경 변경 및 값 저장*/ 
var caf = 3;
function change_firbtn(e) {
    var btns = document.querySelectorAll(".field");
    btns.forEach(function (btn, i) {
      if (e.currentTarget == btn) {
        btn.classList.add("active");
        caf = e.target.value 
        console.log(caf); // 콘솔에 선택한 값 출력하기
      } else {
        btn.classList.remove("active");
      }
    });
}

/* 2번째 질문 페이지 버튼 클릭 시 배경 변경 및 값 저장*/ 
var blend = '';
function change_secbtn(e) {
    var btns = document.querySelectorAll(".field");
    btns.forEach(function (btn, i) {
      if (e.currentTarget == btn) {
        btn.classList.add("active");
        blend = e.target.value
        console.log(blend); // 콘솔에 선택한 값 출력하기
      } else {
        btn.classList.remove("active");
      }
    });
}

/* 3번째 질문 페이지 버튼 클릭 시 배경 변경 및 값 저장*/ 
var notes = '';
function change_thirbtn(e) {
    var btns = document.querySelectorAll(".field");
    btns.forEach(function (btn, i) {
      if (e.currentTarget == btn) {
        btn.classList.add("active");
        notes = e.target.value
        console.log(notes); // 콘솔에 선택한 값 출력하기
      } else {
        btn.classList.remove("active");
      }
    });
}

/* 4번째 질문 페이지 슬라이드 바 값 저장*/ 
/* 신맛 */
var slider1 = document.getElementById("sour");
var output1 = document.getElementById("sour-value");
output1.innerHTML = slider1.value;
        
slider1.oninput = function() {
    output1.innerHTML = this.value;
    console.log(this.value)
}
/* 단맛 */
var slider2 = document.getElementById("sweet");
var output2 = document.getElementById("sweet-value");
output2.innerHTML = slider2.value;
        
slider2.oninput = function() {
    output2.innerHTML = this.value;
    console.log(this.value)
}
/* 쓴맛 */
var slider3 = document.getElementById("bitter");
var output3 = document.getElementById("bitter-value");
output3.innerHTML = slider3.value;
        
slider3.oninput = function() {
    output3.innerHTML = this.value;
    console.log(this.value)
}
/* 바디감 */
var slider4 = document.getElementById("body");
var output4 = document.getElementById("body-value");
output4.innerHTML = slider4.value;
        
slider4.oninput = function() {
    output4.innerHTML = this.value;
    console.log(this.value)
}

/* 변수 값 제출하기 */
function send_result(){

    $.ajax({
        url: '/',
        type: 'GET',
        data: {
            'caf':caf,
            'blend':blend,
            'notes':notes
        },
        datatype: 'json',
    });
}