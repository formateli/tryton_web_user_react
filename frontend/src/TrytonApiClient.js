const TRYTON_SERVER = process.env.REACT_TRYTON_SERVER;

export default class TrytonApiClient {
  constructor(onError) {
    this.onError = onError;
    this.base_url =  TRYTON_SERVER;
  }

  async request(options) {
    let response = await this.requestInternal(options);
    if (response.status === 401 && options.url !== '/tokens') {
      const refreshResponse = await this.put('/tokens', {
        access_token: localStorage.getItem('accessToken'),
      });
      if (refreshResponse.ok) {
        localStorage.setItem('accessToken', refreshResponse.body.access_token);
        response = await this.requestInternal(options);
      }
    }
    if (response.status >= 500 && this.onError) {
      this.onError(response);
    }
    return response;
  }

  async requestInternal(options) {
    let query = new URLSearchParams(options.query || {}).toString();
    if (query !== '') {
      query = '?' + query;
    }

    let response;
    try {
      response = await fetch(options.server + options.url + query, {
        method: options.method,
        headers: {
          'Content-Type': 'application/json',
        //  'Authorization': 'Bearer ' + localStorage.getItem('accessToken'),
        //  ...options.headers,
        },
        //credentials: options.url === '/tokens' ? 'include' : 'omit',
        body: options.body ? JSON.stringify(options.body) : null,
      });
    }
    catch (error) {
      response = {
        ok: false,
        status: 500,
        json: async () => { return {
          code: 500,
          message: 'The server is unresponsive',
          description: error.toString(),
        }; }
      };
    }

    let message
    if (response.status >= 400){
      try {
        message = await response.text()
      }
      catch{
        message = 'Unespected error ocurred. Retry later. (' + response.status + ')'
      }
    }
    else {
      message = response.status !== 204 ? await response.json() : null
    }

    if (response.status >= 400){
      return {
        ok: false,
        status: response.status,
	body: message
      };
    }
    else {
      return {
        ok: response.ok,
        status: response.status,
	body: message
      };
    }
  }

  async get(server, url, query, options) {
    return this.request({method: 'GET', server, url, query, ...options});
  }

  async post(server, url, body, options) {
    return this.request({method: 'POST', server, url, body, ...options});
  }

  async put(server, url, body, options) {
    return this.request({method: 'PUT', server, url, body, ...options});
  }

  async delete(server, url, options) {
    return this.request({method: 'DELETE', server, url, ...options});
  }

  async login(username, password) {
    const response = await this.post('/tokens', null, {
      headers: {
        Authorization:  'Basic ' + btoa(username + ":" + password)
      }
    });
    if (!response.ok) {
      return response.status === 401 ? 'fail' : 'error';
    }
    localStorage.setItem('accessToken', response.body.access_token);
    return 'ok';
  }

  async logout() {
    await this.delete('/tokens');
    localStorage.removeItem('accessToken');
  }

  isAuthenticated() {
    return localStorage.getItem('accessToken') !== null;
  }
}
