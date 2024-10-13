import { useState, useEffect} from 'react'
import './css/update.css'
import Utility from '../welcome_page/utility'

export default function UpdatePost(props){

    const [text, setText] = useState('')

    const handleChange = event =>{
        setText(event.target.value)
    }

    const handleSubmit = event =>{
        event.preventDefault()
        console.log(text)
        console.log('submit')
        setText('')
        if(!('postId' in props.display)){
            console.log('early return')
            console.log(props)
            return
        }
        fetch(`http://localhost:8000/api/post/${props.display.postId}`,{
            method:"PUT",
            headers:{
                'Content-type':'application/json',
                'Authorization':`Token ${localStorage.getItem('token')}`
            },
            body:JSON.stringify({
                'content':text,
                'blog_id':props.display.blogId
            })
        }).then(resp => resp.json())
        .then(data =>{
            console.log(data)
            console.log(data.txt_message)
            console.log(props)
            sendMessage({'data':data, 'type':'update'})
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

    const handleClick = (newMain) =>{
        Utility.changeMain(props.display.setDisplay, newMain);
    }


    return (
        <div className='background'>
            <div className="update-container">
                <div className="update-top-container">
                    <button className="update-decline-button">
                        <div onClick={() =>handleClick('post')}>go back</div>
                    </button>
                    <h1>Update Text </h1>
                </div>
                <div className="update-button-container">
                    <form onSubmit={handleSubmit}>
                        <input onChange={handleChange} value={text} className = "update-search-bar" type="text" name="new-txt" required/>
                        <input className = "update-add-button" type="submit" value="update"/>
                    </form>
                </div>
            </div>
        </div>
    )
}

