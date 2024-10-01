
import './welcome_page/css/styles.css';
import './welcome_page/css/user.css'
import Home from './welcome_page/home';
import Login from './welcome_page/login';
import SignUp from './welcome_page/signup';
import React, {useState, useEffect} from 'react';
import Utility from './welcome_page/utility';

function WelcomePage() {

  const [page, setPage] = useState('home')
  
  //delete the history when pressed back
  useEffect(()=>{
    let storedPage = localStorage.getItem('page')
    //check if the path name is same as local storage
    //if not display path name
    const path = window.location.pathname
    if (!path.includes(storedPage)){
      console.log('includes')
      localStorage.setItem('page', path.substring(1, path.length))
    }else if (storedPage === '/'){
      localStorage.setItem('page', 'home')
    }
    storedPage = localStorage.getItem('page')
    Utility.handleClick({'setter':setPage}, storedPage ? storedPage:'home')
  }, [])
  useEffect(()=>{
    const  deleteHistory = (event) =>{
      setPage(event.state ? event.state.name:'home')
    }
    window.addEventListener('popstate', deleteHistory)

    return () =>{
      window.removeEventListener('popstate', deleteHistory)
    }
  }, [])//remvoe [] if no work

  console.log(window.location.pathname)

  return(
    <div>
      {page === 'home' && <Home  setter={setPage}/>}
      {page === 'login' && <Login  setter={setPage}/>}
      {page === 'signup' && <SignUp  setter={setPage}/>}
    </div>
  )
}

export default WelcomePage;
