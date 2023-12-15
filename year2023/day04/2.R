#!/usr/local/bin/Rscript

# count of matching numbers per card
card_matches <- c()

f <- file("stdin")
open(f)
while (length(line <- readLines(f ,n = 1)) > 0) {
  left <- gsub(".*: (.*) \\|.*", "\\1", line)
  right <- gsub(".*\\| (.*)", "\\1", line)
  
  left_values <- strsplit(left, split = " ") |> unlist()
  right_values <- strsplit(right, split = " ") |> unlist()

  winners <- intersect(left_values, right_values)

  # drop "" from winners, happens when there are two spaces
  # in a row, e.g., "58  5 54"
  winners <- winners[winners != ""]
  card_matches <- c(card_matches, length(winners))
}

print(card_matches)

# calling the number of scratchcards points
# start with one point per originally-issued card
card_points <- rep(1, length(card_matches))

for (i in 1:length(card_points)) {
  if (card_matches[i] > 0) {
    card_points[(i+1):(i + card_matches[i])] = card_points[(i+1):(i + card_matches[i])] + card_points[i]
  }

  print(i)
  print(card_matches[i])
  print(card_points)
}

print(card_points)
print(sum(card_points))