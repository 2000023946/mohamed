
import './css/styles.css';
import './css/user.css'
import Home from './home';
import Login from './login';
import SignUp from './signup';
import React, {useState, useEffect} from 'react';
import Utility from './utility';

function WelcomePage(props) {
  console.log(props)
  
  // //delete the history when pressed back
  // useEffect(()=>{
  //   let storedPage = localStorage.getItem('page')
  //   //check if the path name is same as local storage
  //   //if not display path name
  //   const path = window.location.pathname
  //   if (!path.includes(storedPage)){
  //     localStorage.setItem('page', path.substring(1, path.length))
  //   }else if (storedPage === '/'){
  //     localStorage.setItem('page', 'home')
  //   }
  //   storedPage = localStorage.getItem('page')
  //   Utility.handleClick({'setter':setPage}, storedPage ? storedPage:'home')
  // }, [])
  // useEffect(()=>{
  //   const  deleteHistory = (event) =>{
  //     setPage(event.state ? event.state.name:'home')
  //   }
  //   window.addEventListener('popstate', deleteHistory)

  //   return () =>{
  //     window.removeEventListener('popstate', deleteHistory)
  //   }
  // }, [])//remvoe [] if no work


  return(
    <div>
      {props.page.name === 'home' && <Home  {...props}/>}
      {props.page.name === 'login' && <Login  {...props}/>}
      {props.page.name === 'signup' && <SignUp  {...props}/>}
    </div>
  )
}

export default WelcomePage;
