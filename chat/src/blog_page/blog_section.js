import React, {useState, useEffect} from 'react'
import Blog from './blog'
import Utility from '../welcome_page/utility'
function BlogSection(props){
    let data = props.display.memberData

    const [socket, setSocket] = useState(null)

    const handleClick = (props, blog) =>{
        Utility.isAllowed(props, blog)
        const requestArray = props.display.memberData.request_made
        
        sendMessage(
            requestArray[requestArray.length-1]
        )
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
            console.log('add', data)

            props.display.setDisplay((oldValue) =>{
            return{
                ...oldValue,
                'memberData':{
                ...props.display.memberData,
                'request': [...props.display.memberData.request, data]
                }
            }
            })
            localStorage.setItem('user', JSON.stringify(props.display.memberData))
            console.log('new data', props.display.memberData)

        }
        socket.onclose = event =>{
        console.log(event)
        }
    }, [props.display.memberData.user.username])

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