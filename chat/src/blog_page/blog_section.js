import React, {useState, useEffect} from 'react'
import Blog from './blog'
import Utility from '../welcome_page/utility'
function BlogSection(props){
    let data = props.display.memberData

    const [socket, setSocket] = useState(null)

    const handleClick = (props, blog) =>{
            const acceptUser = () =>{
              Utility.changeMain(props.display.setDisplay, 'post')
                props.post.setPostData({
                    'qs':blog.blog_id
                })
                console.log('allowed')
                error = ''
                
            }
          
              let error = 'Not Allowed. Permission Made for ' + blog.title + ' blog'
              if(blog.state === 'Private'){
                blog.allowed_users.forEach(user => {
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
                  sendMessage({'data':data, 'type':'new request', 'user':data['user_to']['username']})
                  console.log('sent data', data)
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


    useEffect(() =>{
        const socket = new WebSocket(`ws://localhost:8000/ws/request/${props.display.memberData.user.username}/`)
        setSocket(socket)

        socket.onopen = event =>{
        console.log(event)
        }
        socket.onmessage = event =>{
            console.log(event)
            data = JSON.parse(event.data)
            console.log(data)
            if (data['type'] === 'new request'){
                console.log('add', data)
                const newRequestList = props.display.memberData.request
                newRequestList.push(data)
                props.display.setDisplay((oldValue) =>{
                    return{
                        ...oldValue,
                        'memberData':{
                        ...props.display.memberData,
                        'request': newRequestList
                        }
                    }
                })
                localStorage.setItem('user', JSON.stringify(props.display.memberData))
                console.log('new data', props.display.memberData)
            }else if(data['type'] === 'update request'){
                console.log('your reqeust got updated')
                console.log(data)
                fetch(`http://localhost:8000/api/blog/${data.data.blog.blog_id}`,{
                    method:'PUT',
                    headers:{
                        'Content-type':'application/json',
                        'Authorization': `Token ${localStorage.getItem('token')}`
                    },
                    body:JSON.stringify({
                        data
                    })
                }).then(resp => resp.json())
                .then(data =>{
                    console.log(data)
                    props.display.setDisplay(oldValue =>{
                        return {
                            ...oldValue,
                            'memberData':data
                        }
                    })
                    localStorage.setItem('user', JSON.stringify(data))
                    console.log('new props', props)
                })
            }
        }
        socket.onclose = event =>{
        console.log(event)
        }

    }, [])

    const sendMessage = (message) =>{
        socket.send(JSON.stringify(message))
    }

    const displayBlogs = data[props.type].map((blog) =>{
        if (props.type === 'recents'){
            blog = blog['recent_blog']
        }
        return <Blog handleClick={() =>handleClick(props, blog)}  {...blog} key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)}/>
    })
    return (
        <div>
            
            {displayBlogs}
        </div>
    )   
}
export default BlogSection;