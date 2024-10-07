import Utility from "./utility"
import React, {useEffect, useState} from 'react'


export default function SignUp(props){

    const [data, setData] = useState({
        'username':'',
        'email':'',
        'password':'',
        'password2':''
    })

    const [errorData, setErrorData] = useState('');

    function collectData(event){
        event.preventDefault();
        if (data.password === data.password2){
            fetch('http://127.0.0.1:8000/api/signup/', {
                method:'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body:JSON.stringify(JSON.stringify(data))
            }).then(resp => resp.json())
            .then(data =>{
                console.log(data)
                if (data.Success){
                    Utility.handleClick(props.page.setPage, 'login')
                    console.log('success')
                }else{
                    setErrorData(data.Response)
                    console.log('error')
                }
            })
        }
    }
    useEffect(() =>{
        if (data.password !== data.password2){
            setErrorData('Passwords do not match!');
        }
    }, [data.password2])

    const updateData = e => Utility.updateData(e, setData)


    return(
        <div className = "container">
            <div className="user-container">
                <div  className="switch-from" onClick={() => Utility.handleClick(props.page.setPage, 'login')}>Login</div>
                <h2>Sign up</h2>
                {<p>{errorData}</p>}
                <form className="form-container" onSubmit={collectData}>
                        <input onChange={(e) => updateData(e, setData)} className = "text-input" type="text" name="username" placeholder="Enter username" required/>
                        <input onChange={(e) => updateData(e, setData)} className = "text-input" type="email" name="email" placeholder="Email" required/>
                        <input onChange={(e) => updateData(e, setData)} className = "text-input" type="password" name="password" placeholder="Password" required/>
                        <input onChange={(e) => updateData(e,setData)} className = "text-input" type="password" name="password2" placeholder="Re-enter password" required/>
                        <input  className = "submit" type="submit" value="Sign up"/>
                </form>
            </div>
        </div>
    )
}