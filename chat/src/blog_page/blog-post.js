import Post from './post'
import Utility from '../welcome_page/utility'
import { useEffect, useState } from 'react'
export default function BlogPost(props){


    // return(
    //     <Post  {...props} />
    // )

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
                const displayList =  data.post.map(post =>{
                    return <Post key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)} {...post.post_id}/>
                })
                setTitle(data.title)
                setPostList(displayList)
            })
        }
    },[])

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
            setPostList((oldValue) =>{
                return [
                    ...oldValue, <Post key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)} {...data}/>
                ]
            })
            setText('')
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
                let makeNewRecent = true
                props.display.memberData.recents.forEach(recent =>{
                    if(recent.recent_blog.blog_id === blogId){
                        makeNewRecent = false
                    }
                })
                if(makeNewRecent){
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
                    console.log('new recent made')
                    localStorage.setItem('user', JSON.stringify(props.display.memberData))
                }   
                if(!makeNewRecent){
                    console.log('no new recent made')
                }
                console.log('new data', props)
            })
        })
    }


    return(
        <div >
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