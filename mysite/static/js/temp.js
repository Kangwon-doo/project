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


document.addEventListener("DOMContentLoaded", function () {
  const fadeMeElements = document.querySelectorAll("#valbtn");
  const fadeInButtons = document.querySelectorAll("#btn");
  const fadeMeElements2 = document.querySelectorAll(".tohide");

  fadeInButtons.forEach((button) => {
      button.addEventListener("click", function () {
          fadeMeElements.forEach((element) => {
              element.style.transition = "none"; // Remove transition temporarily
              element.style.opacity = "0";
              element.style.transform = "translateY(20px)";
              element.classList.remove("hidden");

              setTimeout(function () {
                  element.style.transition = "opacity 1s, transform 1s"; // Restore transition
                  element.style.opacity = "1";
                  element.style.transform = "translateY(0)";
              }, 10);
          });

          fadeMeElements2.forEach((element) => {
            element.style.transition = "none"; // Remove transition temporarily
            element.style.opacity = "0";
            element.style.transform = "translateY(20px)";
            element.classList.remove("hidden");

            setTimeout(function () {
                element.style.transition = "opacity 1s, transform 1s"; // Restore transition
                element.style.opacity = "1";
                element.style.transform = "translateY(0)";
            }, 10);
        });
      });
  });
  fadeInButtons[0].click();
  fadeInButtons[1].click();
});



/* 1번째 질문 페이지 버튼 클릭 시 배경 변경 및 값 저장*/ 
var caf = 0;
function change_firbtn(e) {
    var btns = document.querySelectorAll(".field1");
    btns.forEach(function (btn, i) {
      if (e.currentTarget == btn) {
        btn.classList.add("active");
        caf = e.target.value 
      } else {
        btn.classList.remove("active");
      }
    });
}

/* 2번째 질문 페이지 버튼 클릭 시 배경 변경 및 값 저장*/ 
var blend = '';
function change_secbtn(e) {
    var btns = document.querySelectorAll(".field2");
    btns.forEach(function (btn, i) {
      if (e.currentTarget == btn) {
        btn.classList.add("active");
        blend = e.target.value
      } else {
        btn.classList.remove("active");
      }
    });
}

/* 3번째 질문 페이지 버튼 클릭 시 배경 변경 및 값 저장*/ 
var notes = '';
function change_thirbtn(elem) {
  var values = document.getElementsByClassName("field3");
  var count = 0;

  for (var i=0;i<values.length;i++){
    if(values[i].classList.contains('active')){ 
        count++;
    }
  }

  if (count>2){
    if (elem.classList.contains('active')){
      elem.classList.remove("active");
      count--;
    }
  } else {
    if (elem.classList.contains('active')){
      elem.classList.remove("active");
    }
    else {
      elem.classList.add("active");
    }
  }
}

/* 4번째 질문 페이지 슬라이드 바 값 저장*/ 
/* 신맛 */
var sour = 3;
var slider1 = document.getElementById("sour");
var output1 = document.getElementById("sour-value");
output1.innerHTML = slider1.value;
        
slider1.oninput = function() {
    output1.innerHTML = this.value;
    sour = this.value;

}
/* 단맛 */
var sweet = 3;
var slider2 = document.getElementById("sweet");
var output2 = document.getElementById("sweet-value");
output2.innerHTML = slider2.value;
        
slider2.oninput = function() {
    output2.innerHTML = this.value;
    sweet = this.value;
}
/* 쓴맛 */
var bitter = 3;
var slider3 = document.getElementById("bitter");
var output3 = document.getElementById("bitter-value");
output3.innerHTML = slider3.value;
        
slider3.oninput = function() {
    output3.innerHTML = this.value;
    bitter = this.value;
}
/* 바디감 */
var body = 3;
var slider4 = document.getElementById("body");
var output4 = document.getElementById("body-value");
output4.innerHTML = slider4.value;
        
slider4.oninput = function() {
    output4.innerHTML = this.value;
    body = this.value;
}

/* 변수 값 제출하기 */
function send_result(){
  var values = document.getElementsByClassName("field3");
  var index = 0;
  const notes = [];

  for (var i=0;i<values.length;i++){
      if(values[i].classList.contains('active')){
          notes[index] = values[i].value;
          index++;
      }
  }
  console.log(notes);

    $.ajax({
        url: '/',
        type: 'GET',
        data: {
            'caf':caf,
            'blend':blend,
            'notes':notes,
            'sour':sour,
            'sweet':sweet,
            'bitter':bitter,
            'body':body
        },
        datatype: 'json',
    });
    alert('결과 페이지로 이동합니다.');
}