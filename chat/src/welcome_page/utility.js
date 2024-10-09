import React, {useEffect} from 'react'

const Utility = {
    handleClick: (setter, display) => handleClick(setter, display),
    updateData: (e, setData) => updateData(e, setData),
    useUpdateHistory: (setPage) => useUpdateHistory(setPage),
    changeMain: (setDisplay, newMain) => changeMain(setDisplay, newMain),
    changePage: (props, name) => changePage(props, name),
    isAllowed: (props, blog) => isAllowed(props, blog)
}

function isAllowed( props, blog){

  const acceptUser = () =>{
    Utility.changeMain(props.display.setDisplay, 'post')
      props.post.setPostData({
          'qs':blog.blog_id
      })
      console.log('allowed')
      error = ''
      
  }

    let error = 'Not Allowed. Permission Made for ' + blog.title + ' blog'
    console.log(blog.allowed_users)
    if(blog.state === 'Private'){
      blog.allowed_users.forEach(user => {
        console.log(user)
        console.log(props)
        if (user.username === props.display.memberData.user.username){
            acceptUser()
        }
    });
    }else{
      acceptUser()
    }

    let makeRequest = true
    let requestPrev = undefined

    props.display.memberData.request_made.forEach((request) =>{
      console.log(blog)
      console.log(request.blog)
      if(request.blog.blog_id === blog.blog_id){
        makeRequest = false
        requestPrev = request
      }
    })

    if (makeRequest && error !== ''){
      //send post to api/request
      fetch('http://localhost:8000/api/request/',{
        method: "POST",
        headers:{
          'Content-type': 'application/json',
          'Authorization': `Token ${localStorage.getItem('token')}`
        },
        body:JSON.stringify({
          'user_from':props.display.memberData.id,
          'user_to': blog.created_user.id,
          'blog': blog.blog_id
        })
      }).then(resp => {
        if (!resp.ok){
          throw new Error(`HTTP error! Status code: ${resp.status}`)
        }
        return resp.json()
      })
      .then(data =>{
        console.log(data)
        const oldRequestList = props.display.memberData.request_made
        oldRequestList.push(data)
        props.display.setDisplay((oldValue) =>{
          return{
            ...oldValue,
            'memberData':{
              ...props.display.memberData,
              'request_made': oldRequestList
            }
          }
        })
        localStorage.setItem('user', JSON.stringify(props.display.memberData))
        console.log(props)
      })
    }
    if (!makeRequest){
      error = `Request Already Made. Status: ${requestPrev.status}`
    }

    props.display.setDisplay((oldValue)=>{
        return{
            ...oldValue,
            'error':error
        }
    })
    console.log(props)
    console.log('not allowed to that blog')
}

function changePage(props, name){
  props.display.setDisplay((oldValue) =>{
      return{
          ...oldValue,
          'main':name
      }
  })
  console.log('page changed')
}

function changeMain(setDisplay, newMain){
  setDisplay((oldDisplay) =>{
    return {
      ...oldDisplay,
      'main':newMain
    }
  })
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