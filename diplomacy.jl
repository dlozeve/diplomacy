import JSON
using DataFrames
using StatsPlots

plotly(size=(1000,700))

territories = JSON.parsefile("territories.json")

years = collect(keys(territories)) |> sort
seasons = territories["1901"] |> keys |> collect
players = territories["1901"]["spring"] |> values |> unique
centres = territories[years[length(years)]]["winter"] |> keys |> collect

centrecounts = DataFrame(player=Symbol[], year=Int[], count=Int[])
for year in years, player in players
    controlled_centres = [c for (c, p) in territories[year]["winter"] if p == player]
    push!(centrecounts, (Symbol(player), parse(Int, year), length(controlled_centres)))
end

centrecounts[centrecounts.player .== :Germany, [:year, :count]]

centrecounts = unstack(centrecounts, :player, :count)

@df centrecounts plot(:year, cols(map(Symbol, players)), xticks=:year, yticks=1:1:20)


units = JSON.parsefile("units.json")

unitcounts = DataFrame(player=Symbol[], year=Int[], armies=Int[], fleets=Int[])
for player in players
    unitcount = Dict(year => length(get(units[year]["winter"], player, [])) for year in years)
    maxcount, maxyear = findmax(unitcount)
    armies = sum([u for (_, u) in units[maxyear]["winter"][player]] .== "A")
    push!(unitcounts, (Symbol(player), parse(Int, maxyear), armies, maxcount - armies))
end


orders = JSON.parsefile("orders.json")

