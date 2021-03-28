"use strict";

var CONFIG = {
    apiUrl: "http://localhost:8000/api/v1"
  };

function PostImage(props){

    return props.images.map(function(image) {
        return (
            <div className="blog-entry ftco-animate">
            <div className="text text-2 pt-2 mt-3">
                <div className="meta-wrap">
                    <p className="meta">
                        <span><a href="/1" className="img" style={{backgroundImage: 'url(/media/user_profile_pics/person3.jpg)', height:"30px", width:"30px", float:"left"}}></a></span>
                        <span><a href="" style={{float:"left",marginLeft:"5%"}}>Harjinder Singh</a></span>   
                    </p>
                </div>
            </div>
            <img src={'/media/' + image.pic} className="img img-2"></img>
            <div className="text text-2 pt-2 mt-3">
                <div className="meta-wrap">
                    <p className="meta">
                        <span>{date.format(new Date(), "YYYY-MM-DD, HH:mm")}</span>
                        <span>
                            <a href="">Like</a>
                        </span>
                        <span><a href="">Comment</a></span>
                    </p>
                </div>
                <p className="mb-4"><a href=""></a><b/></p>
                    
                <div className="comment">
                    <div className="date"><span><b><a href=""></a></b></span></div>
                </div>
                
                <div className="comment">
                    <div className="date"><span><b><a href="">View all comments</a></b></span></div>
                    
                </div>
                    
                    Login to comment!!
            </div>
        </div>
        );
      });
}

function GalleryCustomizer(props) {

    var [images, setImages] = React.useState([{'pic':""}]);
    var [username, setUsername] = React.useState("");

    React.useEffect(function() {
        retrieveUserImages();
      }, []);

    function retrieveUserImages() {
        axios.get(CONFIG.apiUrl + '/images', {
            headers: {
                'Authorization': 'Token beb637498451730a9812fbdff54163f104404e9d'
            }
        }).then(function(response) {
            console.log(response.data.images)
          setImages(response.data.images);
          setUsername(response.data.user);
        });
      }

    return(
        <React.Fragment>
            <div class="col-md-3">
                <PostImage images={images}/>
            </div>
        </React.Fragment>
    );
} 
ReactDOM.render(<GalleryCustomizer/>,
  document.getElementById('root')
);



