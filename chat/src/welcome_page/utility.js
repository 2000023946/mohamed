import React, {useEffect} from 'react'

const Utility = {
    handleClick: (setter, display) => handleClick(setter, display),
    updateData: (e, setData) => updateData(e, setData),
    useUpdateHistory: (setPage) => useUpdateHistory(setPage),
}


function handleClick(setter, display){
  setter(display)
  window.history.pushState({'name':display}, '', display)
  localStorage.setItem('page', display)
  console.log(`page ${display} set`)
}

function updateData(e, setData){
  setData((prevValue) =>{
      return {
          ...prevValue,
          [e.target.name]:e.target.value
      }
  })
}

function useUpdateHistory(setPage){
  //delete the history when pressed back
  useEffect(()=>{
    let storedPage = localStorage.getItem('page')
    //check if the path name is same as local storage
    //if not display path name
    const path = window.location.pathname
    if (!path.includes(storedPage)){
      localStorage.setItem('page', path.substring(1, path.length))
    }else if (storedPage === '/'){
      localStorage.setItem('page', 'home')
    }
    storedPage = localStorage.getItem('page')
    handleClick(setPage, storedPage ? storedPage:'home')
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
}

export default Utility;