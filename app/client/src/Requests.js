/*
    Simple request wrapper around the  browser native fetch API.
    This class may never exist on release state (in exchange for a more robust API),
    but for the time being, it will be the main source of requests for the backend API.
*/
class JsonApiReq{

    domain_name = null;
    endpoint = null;
    https=false;
    debug=false;
    constructor(domain, endpoint=null, use_https=false, debug=false){
        this.domain_name = domain;
        this.endpoint = endpoint;
        this.https = use_https;
        this.debug = debug;
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
        if(this.debug) alert(`REQUEST DEBUG->${url} : ${opt.toString()}`);
        let req = new Request(url, opt);
        if(this.debug) alert(req);
        return fetch(req).then((response) => {
            return response.json();
        });
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
        if(this.debug===true) alert(`REQUEST DEBUG->${url} : ${opt}`);
        let req = new Request(url, opt);

        return fetch(req).then((response) => {
            return response.json();
        });
    }
}
export default JsonApiReq;
