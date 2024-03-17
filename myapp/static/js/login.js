const wrapper = document.querySelector('.wrapper');
const login = document.querySelector('.login-link');
const register = document.querySelector('.register-link');

register.addEventListener('click',()=>{
wrapper.classList.add('active');

});


login.addEventListener('click',()=>{
    wrapper.classList.remove('active');
    
});
