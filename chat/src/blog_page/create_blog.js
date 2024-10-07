import { useState } from "react"
import Utility from "../welcome_page/utility"



export default function CreateBlog(props){

    const [data, setData] = useState({})

    const updateData = event =>{
        setData(oldValue =>{
            return {
                ...oldValue,
                [event.target.name]: event.target.value
            }
        })
    }

    const [error, setError] = useState('')

    function validData (){
        if (!['public', 'private'].includes(data.state.toLowerCase())){
            setError('Enter Valid State. Either "public" or "private"')
            return false
        }
        return true
    }

    const submitData = (event) =>{
        event.preventDefault()
        if (!validData()){
            return
        }
        fetch(`http://localhost:8000/api/blog/`, {
            method: 'POST',
            headers:{
                'Content-type':'application/json',
                'Authorization': `Token ${localStorage.getItem('token')}`
            },
            body:JSON.stringify({ ...data})
        }).then(resp => resp.json())
        .then(respData =>{
            console.log(respData)
            props.post.setPostData((oldValue) =>{
                return {
                    ...oldValue,
                    'qs':respData.blog_id
                }
            })
            Utility.changePage(props, 'post')
        })

    }


    return(
        <div className="div-container">
            <div className = "container">
                <div className="user-container">
                    <div onClick={() => Utility.changePage(props, 'home')} className="switch-from">Go Back</div>
                <h2>Create a Blog</h2>
                    <p>{error !== '' && error}</p>
                <form className="form-container" onSubmit={submitData}>
                        <input onChange={updateData} className = "text-input" type="text" name = "title" placeholder="Title" required/>
                        <input onChange={updateData} className = "text-input" type="text" name = "description" placeholder="description" required/>
                        <input onChange={updateData} className = "text-input" type="text" name = "state" placeholder="public or private"/>
                        <input className = "submit" type="submit" value="create"/>
                </form>
                </div>
            </div>
        </div>
    )
}