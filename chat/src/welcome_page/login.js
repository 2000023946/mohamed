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
        console.log('data sent!')
        console.log(data)
        fetch('http://127.0.0.1:8000/api/login/', {
            method:'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body:JSON.stringify(JSON.stringify(data))
        }).then(resp => resp.json())
        .then(data =>{
            console.log(data)
            if (data.Success){
                console.log('success')
            }else{
                console.log('failed')
            }
            setErrorData({
                'isError':!data.Success,
                'error':data.Response
            })
            fetch(`http://127.0.0.1:8000/api/member/${data.User_Id}`,{
                method:'GET',
                headers: {
                    "Authorization": `Token ${data.Token}`
                },
            }).then(resp => resp.json())
            .then(data =>
                console.log(data)
            )
        })
    }

    const updateData = (event) => Utility.updateData(event, setData)

    return(
        <div className='container'>
            <div className="user-container">
                <div className="switch-from" onClick={() => Utility.handleClick(props, 'signup')}>Sign up</div>
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
