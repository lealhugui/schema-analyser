/*
    Simple request wrapper around the  browser native fetch API.
    This class may never exist on release state (in exchange for a more robust API),
    but for the time being, it will be the main source of requests for the backend API.
*/ 
class JsonApiReq{

    domain_name = null;
    endpoint = null;
    https=false;
    constructor(domain, endpoint=null, use_https=false){
        this.domain_name = domain;
        this.endpoint = endpoint;
        this.https = use_https;
    }

    get(){
        let opt = {
            method: 'GET',
            headers: new Headers(),
            mode: 'cors',
            cache: 'default'
        };

        let url = ((this.https ? "https://" : "http://") +
            this.domain_name +
            (this.domain_name.substring(this.domain_name.length-1,1) === "/" ? "" : "/") +
            (this.endpoint));
        let req = new Request(url, opt);

        return fetch(req).then((response) => {
            return response.json();
        })
    }
    post(payload=null){
        let opt = {
            method: 'POST',
            headers: new Headers(),
            mode: 'cors',
            cache: 'default'
        };
        let url = ((this.https ? "https://" : "http://") +
            this.domain_name +
            (this.domain_name.substring(this.domain_name.length-1,1) === "/" ? "" : "/") +
            (this.endpoint));
        let req = new Request(url, opt);

        return fetch(req).then((response) => {
            return response.json();
        })
    }
}
export default JsonApiReq;