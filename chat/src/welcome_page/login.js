import Utility from './utility'
import React, {useState} from 'react'

export default function Login(props){

    const [data, setData] = useState({
        'username':'',
        'password':'',
    })

    const [errorData, setErrorData] = useState({
        'isError':false,
        'error':''
    });

    function collectData(event){
        event.preventDefault();
        fetch('http://127.0.0.1:8000/api/login/', {
            method:'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body:JSON.stringify(JSON.stringify(data))
        }).then(resp => resp.json())
        .then(data =>{
            setErrorData({
                'isError':!data.Success,
                'error':data.Response
            })
            return fetch(`http://127.0.0.1:8000/api/member/${data.User_Id}`,{
                method:'GET',
                headers: {
                    "Authorization": `Token ${data.Token}`
                },
            }).then(resp => resp.json())
            .then(memberData =>{
                props.display.setDisplay({
                    'name':'BlogHome',
                    'memberData':memberData
                })
                Utility.handleClick(props.page.setPage, memberData.user.username)
                console.log(memberData)
                localStorage.setItem(memberData.user.username, JSON.stringify(memberData))
            })
        })
    }

    const updateData = (event) => Utility.updateData(event, setData)

    return(
        <div className='container'>
            <div className="user-container">
                <div className="switch-from" onClick={() => Utility.handleClick(props.page.setPage, 'signup')}>Sign up</div>
                <h2>Login</h2>
                {errorData.isError && <p>{errorData.error}</p>}
                <form className="form-container" onSubmit={collectData}>
                        <input onChange={updateData} className = "text-input" type="text" name="username" placeholder="Enter username" required/>
                        <input onChange={updateData} className = "text-input" type="password" name="password" placeholder="Password" required/>
                        <input className = "submit" type="submit" value="Login"/>
                </form>
            </div>

        </div>
    )
}
