console.log("hello world")

const modalBtns = [...document.getElementsByClassName("modal-button")]
const modalBody = document.getElementById("modal-body-confirm")
const startBtn=document.getElementById("start")
const url=window.location.href
console.log("hello");
modalBtns.forEach((modalBtn) =>
  modalBtn.addEventListener("click", () => {
    console.log("hello")
    console.log(modalBtn)
    const pk = modalBtn.getAttribute("data-pk")
    const name = modalBtn.getAttribute("data-quiz")
    const num_of_Questions = modalBtn.getAttribute("data-questions")
    const difficulty = modalBtn.getAttribute("data-difficulty")
    const time = modalBtn.getAttribute("data-time") 

    modalBody.innerHTML = `
<div class="h5 mb-3"> Are you sure you want to begin <b>${name}</b>?</div>
<div class="text-muted">
<ul>
<li>difficulty: <b>${difficulty}</b></li>
<li>number: <b>${num_of_Questions}</b></li>

<li>Time: <b>${time}</b> min</li>
<ul>
</div>
`

startBtn.addEventListener('click',()=>
{window.location.href=url+pk
  })

  }))
