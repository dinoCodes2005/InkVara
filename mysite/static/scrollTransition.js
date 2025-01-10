
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.classList.add('showLeft');
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
hiddenElements2.forEach((el) => observer.observe(el));