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
            localStorage.setItem('token', data.Token)
            return fetch(`http://127.0.0.1:8000/api/member/${data.User_Id}`,{
                method:'GET',
                headers: {
                    "Authorization": `Token ${localStorage.getItem('token')}`
                },
            }).then(resp => resp.json())
            .then(memberData =>{
                props.display.setDisplay({
                    'name':'BlogHome',
                    'main':'home',
                    'memberData':memberData
                })
                const user = memberData.user.username ? 'unkown_user': memberData.user.username
                Utility.handleClick(props.page.setPage, user)
                console.log(memberData)
                localStorage.setItem('user', JSON.stringify(memberData))
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
