import Post from './post'
import Utility from '../welcome_page/utility'
import { useEffect, useState } from 'react'
export default function BlogPost(props){


    // return(
    //     <Post  {...props} />
    // )
    console.log(props)
    const [postList, setPostList] = useState([])

    const [text, setText] = useState('')
    const [title, setTitle] = useState('')

    const [blogId, setBlogId] = useState(props.post.postData.qs)

    useEffect(() =>{
        console.log(blogId)
        if (blogId){
            fetch(`http://localhost:8000/api/blog/${blogId}`, {
                method: 'GET',
                headers:{
                    'Authorization': `Token ${localStorage.getItem('token')}`
                }
            }).then(resp => resp.json())
            .then(data =>{
                props.post.setPostData((oldValue) => {
                    return {
                        ...oldValue,
                        data
                    }
                })
                console.log(data)
                props.display.setDisplay(oldValue =>{
                    return {
                        ...oldValue,
                        'blogId':data.blog_id
                    }
                })
                const displayList =  data.post.map(post =>{
                    return <Post key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)} {...props} {...post}/>
                })
                setTitle(data.title)
                setPostList(displayList)
            })
        }
    },[])


    const [data, setData] = useState({
        'socket':null,
        'send': {'type':'msg'},
        'recieve': []
    })

    useEffect(() =>{
        const socket = new WebSocket(`ws://localhost:8000/ws/chat_room/${blogId}/`)
        setData(oldValue =>{
            return {
                ...oldValue,
                'socket':socket
            }
        })
        socket.onopen = event =>{
            console.log(event)
        }
        socket.onmessage = event =>{
            const data = JSON.parse(event.data)
            console.log('dat recv', data)
            if (data['type'] === 'msg'){
                setPostList((oldValue) =>{
                    return [
                        ...oldValue, <Post key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)} {...props} {...data}/>
                    ]
                })
            }else if (data['type'] === 'update'){
                const newPostList = data['data']['post'].map(post =>{
                    return <Post key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)} {...props} {...post}/>
                })
                setPostList(newPostList)
                console.log(postList, newPostList)
            }else if(data['type'] === 'remove'){
                const newPostList = data['data']['post'].map(post =>{
                    return <Post key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)} {...props} {...post}/>
                })
                setPostList(newPostList)
                console.log(postList, newPostList)
            }
        }
        socket.close = event =>{
            console.log(event)
        }
    }, [])

    const sendMessage = (message) =>{
        data.socket.send(JSON.stringify(message))
    }

    console.log(props)

    const collectData = (event) =>{
        setText((oldText) =>{
            return event.target.value
        })
        console.log(event.target.value)
    }

    const sendPostData = (event) =>{
        event.preventDefault()
        fetch(`http://localhost:8000/api/post/`, {
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
                'Authorization': `Token ${localStorage.getItem('token')}`
            },
            body:JSON.stringify({
                'username':props.display.memberData.user.username,
                'text_message':`${text}, ${blogId}`
            })
        }).then(resp => resp.json())
        .then(data => {
            console.log(data)
            console.log('new props', props)
            setText('')
            const sendData = {
                ...data,
                'type':'msg',
            }
            sendMessage(sendData)
        event.preventDefault()
        fetch(`http://localhost:8000/api/recent/`, {
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
                'Authorization': `Token ${localStorage.getItem('token')}`
            },
            body:JSON.stringify({
                'user_for':`${props.display.memberData.user.user_id}`,
                'blog_id': `${blogId}`,
            })
        }).then(resp => resp.json())
            .then(data =>{
                console.log('new recent', data)
                if(data['recent_id'] !== -1){
                    let oldRecentList = props.display.memberData.recents
                    oldRecentList.push(data)
                    props.display.setDisplay(oldValue =>{
                        return {
                            ...oldValue,
                            memberData:{
                                ...props.display.memberData,
                                'recents': oldRecentList
                            }
                        }
                    })
                    localStorage.setItem('user', JSON.stringify(props.display.memberData))
                }else{
                    console.log('no new recent')
                }
            })
        })
    }


    return(
        <div>
            <div className="post-content-title">
                <div className='post-title-container'>
                    {title !== '' && <h1> {title}</h1>}
                    <p className='post-on-back' onClick={() => Utility.changePage(props, 'home')}>Go Back</p>
                </div>
                <h3>{props.post.postData.description} </h3>  
            </div>
            <div className="post-text-container">
                <div className="post-add-container">
                        {postList.reverse()}
                    <div className="post-form-container">
                        <form className = "post-form-content" onSubmit={sendPostData}>
                            <div>
                                <input onChange={collectData}className="post-search-bar" type="text" value={text} name="message" placeholder="Send message" required/>
                                <input className="post-add-button" type="submit" value="add"/>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}