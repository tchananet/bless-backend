const baseUrl = '127.0.0.1:8000/'

const getServices = async () => {
  try {
    // const response = await fetch(`${baseUrl}service_list/`)
    const response = await fetch(`http://localhost:8000/service_list/?format=json`, {
      // mode: 'no-cors',
      headers: {
        // 'Access-Control-Allow-Origin':'*'
      }
    })
    response.json().then((res)=>{
      console.log(res)
      res.forEach((service)=>{
        console.log(service)
        const holder = `
                          <div class="card" style="background-image: url(${'https://loremflickr.com/966/966/business'});">
                              <div class="card-body">
                                <h5 class="card-title">
                                  <a href="">${service.name}</a>
                                </h5>
                                <p class="card-text">${service.description}</p>
                                <div class="read-more">
                                  <a href="#"><i class="icofont-arrow-right"></i> Read More</a>
                                </div>
                              </div>
                          </div>
                    `
        const servicesContainer = document.getElementById("servicesContainer")
        const serviceCard = document.createElement('div')
        serviceCard.setAttribute('class', 'col-md-4 d-flex align-items-stretch mt-4 mt-md-0')
        serviceCard.setAttribute('data-aos', 'fade-up') 
        serviceCard.innerHTML=holder
        servicesContainer.appendChild(serviceCard)

      })
    }).catch((error)=>{
      console.error(error)
    })
    console.log(response)
  }
  catch (error) {
    console.log(error)
  }
}
getServices()

const team_holder = `<div class="col-md-4">
                    <div class="team-player">
                      <img src="assets/img/team/team-1.jpg" alt="Thumbnail Image" class="rounded-circle img-fluid img-raised" style="width: 150px; height: 150px;">
                      <h4 class="title">Achu Pessong Bless</h4>
                      <p class="category text-primary">Directeur Generale/ Fondateur</p>
                      <p class="description">You can write here details about one of your team members. You can give more details about what they do. Feel free to add some
                        <a href="#">links</a> for people to be able to follow them outside the site.</p>
                      <a href="#pablo" class="btn btn-primary btn-icon btn-round"><i class="fab fa-twitter"></i></a>
                      <a href="#pablo" class="btn btn-primary btn-icon btn-round"><i class="fab fa-instagram"></i></a>
                      <a href="#pablo" class="btn btn-primary btn-icon btn-round"><i class="fab fa-facebook-square"></i></a>
                    </div>
                  </div>`

const getTeams = async () => {
  try {
    // const response = await fetch(`${baseUrl}service_list/`)
    const response = await fetch(`http://localhost:8000/team_list/?format=json`, {
      // mode: 'no-cors',
      headers: {
        // 'Access-Control-Allow-Origin':'*'
      }
    })
    response.json().then((res)=>{
      console.log(res)
      res.forEach((member)=>{
        console.log(member)
        const holder = `
                          <div class="team-player">
                            <img src="${member.image}" alt="Thumbnail Image" class="rounded-circle img-fluid img-raised" style="width: 150px; height: 150px;">
                            <h4 class="title">${member.name}</h4>
                            <p class="category text-primary">${member.position}</p>
                            <p class="description">${member.description}</p>
                            <a href="#pablo" class="btn btn-primary btn-icon btn-round"><i class="fab fa-twitter"></i></a>
                            <a href="#pablo" class="btn btn-primary btn-icon btn-round"><i class="fab fa-instagram"></i></a>
                            <a href="#pablo" class="btn btn-primary btn-icon btn-round"><i class="fab fa-facebook-square"></i></a>
                          </div>
                   `
        const teamContainer = document.getElementById("team-container")
        const teamCard = document.createElement('div')
        teamCard.setAttribute('class', 'col-md-4')
        teamCard.setAttribute('data-aos', 'fade-up') 
        teamCard.innerHTML=holder
        teamContainer.appendChild(teamCard)

      })
    }).catch((error)=>{
      console.error(error)
    })
    console.log(response)
  }
  catch (error) {
    console.log(error)
  }
}

getTeams()