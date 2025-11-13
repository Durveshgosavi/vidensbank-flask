"""
Script to create the advanced calculator template
"""

template = """{% extends "base.html" %}

{% block title %}Klimaberegner | Vidensbank{% endblock %}

{% block content %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">

<style>
.calculator-hero {
    background: linear-gradient(135deg, #2E8B57 0%, #4CAF50 100%);
    color: white;
    padding: 4rem 2rem;
    text-align: center;
}
.calc-card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 12px 36px rgba(46, 139, 87, 0.08);
    margin-bottom: 2rem;
}
.meat-bar {
    height: 50px;
    border-radius: 10px;
    display: flex;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.meat-segment {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
}
.segment-red { background: linear-gradient(135deg, #c0392b, #e74c3c); }
.segment-bright { background: linear-gradient(135deg, #e67e22, #f39c12); }
.segment-fish { background: linear-gradient(135deg, #3498db, #5dade2); }
.segment-veg { background: linear-gradient(135deg, #27ae60, #2ecc71); }
</style>

<div class="calculator-hero">
    <h1>🌱 Avanceret Klimaberegner</h1>
    <p>CONCITO data • AI-anbefalinger • Besparelsespotentiale</p>
</div>

<div class="container" style="max-width: 1200px; margin: 2rem auto;">
    <div class="calc-card">
        <h2>Kantine Parametre</h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
            <div>
                <label>Medarbejdere</label>
                <input type="number" id="employees" value="150" class="form-control">
            </div>
            <div>
                <label>Fremmøde (%)</label>
                <input type="number" id="attendance" value="85" class="form-control">
            </div>
            <div>
                <label>Driftsdage/år</label>
                <input type="number" id="operating_days" value="240" class="form-control">
            </div>
        </div>
    </div>

    <div class="calc-card">
        <h2>Kødfordeling</h2>
        <div class="meat-bar" id="meatBar">
            <div class="meat-segment segment-red" id="segmentRed" style="width:30%">Rødt 30%</div>
            <div class="meat-segment segment-bright" id="segmentBright" style="width:40%">Lyst 40%</div>
            <div class="meat-segment segment-fish" id="segmentFish" style="width:15%">Fisk 15%</div>
            <div class="meat-segment segment-veg" id="segmentVeg" style="width:15%">Veg 15%</div>
        </div>
        <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-top:1rem;">
            <div><label>Rødt</label><input type="range" id="redMeat" min="0" max="70" value="30" step="5"><div id="redVal">30%</div></div>
            <div><label>Lyst</label><input type="range" id="brightMeat" min="0" max="70" value="40" step="5"><div id="brightVal">40%</div></div>
            <div><label>Fisk</label><input type="range" id="fish" min="0" max="50" value="15" step="5"><div id="fishVal">15%</div></div>
            <div><label>Veg</label><input type="range" id="vegetarian" min="5" max="100" value="15" step="5"><div id="vegVal">15%</div></div>
        </div>
        <div style="text-align:center; margin-top:1rem;">Total: <span id="total">100</span>%  <span id="warn" style="color:red; display:none;">Skal være 100%!</span></div>
    </div>

    <button class="btn btn-success btn-lg" onclick="calc()" style="display:block; margin:2rem auto; padding:1rem 3rem;">Beregn</button>

    <div id="results" style="display:none;">
        <div class="calc-card" style="background:linear-gradient(135deg,#2E8B57,#4CAF50); color:white;">
            <h2 style="color:white; text-align:center;">Resultater</h2>
            <div style="text-align:center; font-size:3rem; font-weight:700;" id="mainRes">-</div>
            <div style="text-align:center;">kg CO2e per måltid</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:2rem;">
                <div style="background:rgba(255,255,255,0.15); padding:1.5rem; border-radius:12px; text-align:center;">
                    <div style="font-size:2rem; font-weight:700;" id="tons">-</div>
                    <div>Tons/år</div>
                </div>
                <div style="background:rgba(255,255,255,0.15); padding:1.5rem; border-radius:12px; text-align:center;">
                    <div style="font-size:2rem; font-weight:700;" id="savings">-</div>
                    <div>DKK besparelse/år</div>
                </div>
            </div>
        </div>
        <div class="calc-card">
            <h2>AI Anbefalinger</h2>
            <div id="recs"></div>
        </div>
    </div>
</div>

<script>
let dist = {r:30, b:40, f:15, v:15};
function upd(){
    let r=+document.getElementById('redMeat').value;
    let b=+document.getElementById('brightMeat').value;
    let f=+document.getElementById('fish').value;
    let v=+document.getElementById('vegetarian').value;
    let t=r+b+f+v;
    document.getElementById('redVal').textContent=r+'%';
    document.getElementById('brightVal').textContent=b+'%';
    document.getElementById('fishVal').textContent=f+'%';
    document.getElementById('vegVal').textContent=v+'%';
    document.getElementById('total').textContent=t;
    document.getElementById('segmentRed').style.width=r+'%';
    document.getElementById('segmentBright').style.width=b+'%';
    document.getElementById('segmentFish').style.width=f+'%';
    document.getElementById('segmentVeg').style.width=v+'%';
    document.getElementById('segmentRed').textContent=r>8?'Rødt '+r+'%':'';
    document.getElementById('segmentBright').textContent=b>8?'Lyst '+b+'%':'';
    document.getElementById('segmentFish').textContent=f>8?'Fisk '+f+'%':'';
    document.getElementById('segmentVeg').textContent=v>8?'Veg '+v+'%':'';
    document.getElementById('warn').style.display=t!==100?'inline':'none';
    dist={r,b,f,v};
}
async function calc(){
    if(dist.r+dist.b+dist.f+dist.v!==100){alert('Total skal være 100%'); return;}
    try{
        let res=await fetch('/api/calculate-canteen-impact',{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({
                employees:+document.getElementById('employees').value,
                attendance_rate:+document.getElementById('attendance').value/100,
                operating_days:+document.getElementById('operating_days').value,
                meals_per_day:1,
                meat_distribution:{red_meat_percent:dist.r,bright_meat_percent:dist.b,fish_percent:dist.f,vegetarian_percent:dist.v},
                portion_sizes:{protein_gram:120,vegetables_gram:200,carbs_gram:150},
                organic_percent:{meat:40,vegetables:60,dairy:30},
                waste:{preparation:8,plate:12,buffet:5},
                local_sourcing:60,
                seasonal_produce:50
            })
        });
        let d=await res.json();
        if(d.success){
            document.getElementById('results').style.display='block';
            document.getElementById('mainRes').textContent=d.results.per_meal_kg.toFixed(2);
            document.getElementById('tons').textContent=d.results.annual_tons.toFixed(1);
            document.getElementById('savings').textContent=Math.round(d.results.estimated_cost_savings_dkk).toLocaleString();
            let h='';
            d.results.recommendations.forEach(r=>{
                h+=`<div style="background:#f8f9fa; padding:1.5rem; border-radius:8px; margin-bottom:1rem; border-left:4px solid #2E8B57;">
                    <div style="font-weight:700; margin-bottom:0.5rem;">${r.priority}. ${r.title}</div>
                    <div style="color:#7f8c8d; margin-bottom:0.75rem;">${r.description}</div>
                    <div><strong>${r.annual_saving_tons.toFixed(1)} tons/år</strong> • ${r.implementation_time} • ${r.difficulty}</div>
                </div>`;
            });
            document.getElementById('recs').innerHTML=h;
            document.getElementById('results').scrollIntoView({behavior:'smooth'});
        }
    }catch(e){alert('Fejl: '+e.message);}
}
['redMeat','brightMeat','fish','vegetarian'].forEach(id=>document.getElementById(id).addEventListener('input',upd));
upd();
</script>
{% endblock %}
"""

with open('templates/calculator.html', 'w', encoding='utf-8') as f:
    f.write(template)

print('[OK] Calculator template created successfully!')
