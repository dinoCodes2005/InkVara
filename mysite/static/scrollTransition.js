
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.classList.add('showLeft');
        }
        else{
            entry.target.classList.remove('showLeft');
        }

    })
})
const hiddenElements = document.querySelectorAll('.hiddenLeft');
hiddenElements.forEach((el) => observer.observe(el)); // This line is correct


const observer2 = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.classList.add('showRight');
        }
        else{
            entry.target.classList.remove('showRight');
        }
    })
})
const hiddenElements2 = document.querySelectorAll('.hiddenRight');
hiddenElements2.forEach((el) => observer2.observe(el));



const observer3 = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.classList.add('showPop');
        }
        else{
            entry.target.classList.remove('showPop');
        }
    })
})
const hiddenElements3 = document.querySelectorAll('.hiddenPop');
hiddenElements3.forEach((el) => observer3.observe(el));