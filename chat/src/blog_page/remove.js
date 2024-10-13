import Utility from '../welcome_page/utility'
import './css/remove.css'
import {useState, useEffect} from 'react'
export default function RemovePost(props){

    const formData = true

    const handleSubmit = event =>{
        event.preventDefault()
        console.log('submit')
        if(!('postId' in props.display)){
            console.log('early return')
            console.log(props)
            return
        }
        fetch(`http://localhost:8000/api/post/${props.display.postId}`,{
            method:"DELETE",
            headers:{
                'Content-type':'application/json',
                'Authorization':`Token ${localStorage.getItem('token')}`
            },
            body:JSON.stringify({
                'remove':formData,
                'blog_id':props.display.blogId
            })
        }).then(resp => resp.json())
        .then(data =>{
            console.log(data)
            console.log(data.txt_message)
            console.log(props)
            sendMessage({'data':data, 'type':'remove'})
            Utility.changeMain(props.display.setDisplay, 'post')
        })
    }

    const [socket, setSocket] = useState(null)

    useEffect(() =>{
        const socket = new WebSocket(`ws://localhost:8000/ws/chat_room/${props.display.blogId}/`)
        setSocket(socket)

        socket.onopen = event =>{
        console.log(event)
        }
        socket.onmessage = event =>{
            console.log(event)
        }
        socket.onclose = event =>{
        console.log(event)
        }

    }, [])

    const sendMessage = (message) =>{
        socket.send(JSON.stringify(message))
    }

    
    return(
        <div className="remove-background">
             <div className="remove-container">
                <h1>Confirm to Remove </h1>
                <div className="remove-button-container">
                    <button className="remove-decline-button">
                        <div onClick={() => Utility.changeMain(props.display.setDisplay, 'post')}>go back</div>
                    </button>
                    <form onSubmit={handleSubmit}>
                        <input className = "remove-accept-button" type="submit" value='Remove'/>
                    </form>
                </div>
            </div>
        </div>
    )
}