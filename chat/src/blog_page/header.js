import React, {useState} from 'react'
import Utility from '../welcome_page/utility';

function Header(props){
    console.log(props)

    const goLogin = (event) =>{
        props.display.setDisplay((oldValue) =>{
            return{
                ...oldValue,
                'main':"",
                'name':'WelcomePage'
            }
        })
        props.page.setPage('login')
    }

    const [size, setSize] = useState()
    const changeStyle = (event) =>{
        setSize({
            'width': '300px',
        })
    }
    const [searchData, setSearchData] = useState()

    const changeData = (event) =>{
        setSearchData(event.target.value)
    }

    const submitData = (event) =>{
        event.preventDefault();
        console.log(searchData)
        fetch(`http://localhost:8000/api/blog/search/?q=${searchData}`,{
            headers:{
                'Authorization': `Token ${localStorage.getItem('token')}`
            }
        }).then(resp => resp.json())
        .then(data =>{
            console.log(data)
            const newMemberData = {
                ...props.display.memberData,
                'search_data': data,
            }
            props.display.setDisplay((oldValue) =>{
                return {
                    ...oldValue,
                    'memberData':newMemberData
                }
            })
            Utility.changePage(props, 'search')
        })
    }


    console.log(props.display.error)

    return (
        <div>
            <h1 className = "welcome-message">
            <div style={{'cursor':'pointer'}} onClick={(e) => Utility.changePage(props, 'home')}>
                Welcome to {props.username} BlogSpace!
            </div>
            </h1>
            <div className="header">
                <div className="left-header">
                    <button onClick={(e) => Utility.changePage(props, 'create_blog')} className="create-button">
                        <div>Create new Blog</div>
                    </button>
                </div>
                <div className="middle-header">
                    <form  onSubmit={submitData}>
                        <div className="search-bar">
                            <input onChange={changeData} onMouseEnter={changeStyle} style={size} id="search" type="search" name="q" placeholder="Search"/>
                            <input className = "search-button" type="submit" value="submit"/>
                        </div>
                    </form>
                    <p>{props.display.error}</p>
                </div>
                <div className="right-header">
                    <button className="notification-button">
                        <div onClick={(e) => Utility.changePage(props, 'notification')}>
                        Notifications
                        <p className="num-requests"> num_requests </p>
                        </div>
                    </button>
                    <button className="logout-button">
                        <div onClick={goLogin}>Log out</div>
                    </button>
                </div>
            </div>
        </div>
    )
}

export default Header;
