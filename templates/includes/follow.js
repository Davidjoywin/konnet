document.addEventListener('DOMContentLoaded', () => {
  const follow_fnd = document.querySelector('.follow-friend');

    const follow_bttn = document.querySelector('a');
    follow_bttn.addEventListener('click', (e) => {
      e.preventDefault();
      if (follow_fnd.innerText === 'follow') {
        follow_fnd.innerText = 'following';
        setTimeout(()=> {
          follow_fnd.style.display = 'none';
        }, 5000)
        console.log(follow_fnd);
      } else {
        follow_fnd.innerText = 'follow';
        console.log(follow_fnd);
      }
    })

    // const form = document.querySelector('form');

    // form.addEventListener('submit', (event) => {
    //   event.preventDefault();
    //   let text = document.querySelector('#text');
    //   console.log(text.value);
    //   text.value = '';
    // })

    const menu_bttn = document.querySelector(".menu-bttn");
    const menu = document.querySelector(".menu");
    const html = document.querySelector("html");

    menu_bttn.addEventListener('click', () => {
      const menu_classes = menu_bttn.classList.value.split(' ');
      if (!menu_classes.includes('visited')){

        // add the visited class to the menu_bttn
        // using concatenation
        menu_bttn.classList.value += ' visited';
        menu.style.display = 'block';
      } else {
        // exclude the visited class
        menu_bttn.classList.value = menu_classes[0];
        menu.style.display = 'none';
      }
    })

    // html.addEventListener('click', () => {
    //   if (getComputedStyle(menu).display === 'block')
    //     menu.style.display = 'none';
    //     console.log("html cliked")
    // })
})